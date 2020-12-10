import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecs from '@aws-cdk/aws-ecs';
import * as rds from '@aws-cdk/aws-rds';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as ecs_patterns from '@aws-cdk/aws-ecs-patterns';
import { DockerImageAsset } from '@aws-cdk/aws-ecr-assets';
import { join } from 'path';
import * as cdk from '@aws-cdk/core';

export class CdkProjectStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, "Vpc", {
      maxAzs: 2,
      natGateways: 0,
    });
    
    const rdsInstance = new rds.DatabaseInstance(this, "Database", {
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0_19,
      }),
      vpc: vpc,
      databaseName: 'CdkProjectRds',
      deleteAutomatedBackups: true,
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T2,
        ec2.InstanceSize.MICRO
      ),
      vpcSubnets: {
        subnetType: ec2.SubnetType.ISOLATED,
      },
      allocatedStorage: 10,
      credentials: {
        username: "admin",
      },
    });
    
    const image = new DockerImageAsset(this, "DockerImage", {
      directory: join(__dirname, "..", "microblog"),
    });
    
    const cluster = new ecs.Cluster(this, "EcsCluster", { vpc: vpc });

    const taskDefinition = new ecs.FargateTaskDefinition(this, "TaskDef");

    const container = taskDefinition.addContainer("WebContainer", {
      image: ecs.ContainerImage.fromDockerImageAsset(image),
      memoryLimitMiB: 512,
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: "cdk-ecs" }),
      environment: {
        DB_NAME: "CdkProjectRds",
      },
      secrets: {
        DB_ENGINE: ecs.Secret.fromSecretsManager(rdsInstance.secret!, "engine"),
        DB_HOST: ecs.Secret.fromSecretsManager(rdsInstance.secret!, "host"),
        DB_PORT: ecs.Secret.fromSecretsManager(rdsInstance.secret!, "port"),
        DB_USERNAME: ecs.Secret.fromSecretsManager(
          rdsInstance.secret!,
          "username"
        ),
        DB_PASSWORD: ecs.Secret.fromSecretsManager(
          rdsInstance.secret!,
          "password"
        ),
      },
    });
    container.addPortMappings({
      containerPort: 8080,
    });

    const fargeteService = new ecs.FargateService(this, "FargateService", {
      cluster: cluster,
      taskDefinition: taskDefinition,
      assignPublicIp: true,
    });

    const lb = new elbv2.ApplicationLoadBalancer(this, "LB", {
      vpc: vpc,
      internetFacing: true,
    });
    const listener = lb.addListener("Listener", { port: 80 });
    listener.addTargets("ECS", {
      port: 8080,
      targets: [fargeteService],
    });
    
    rdsInstance.connections.allowFrom(fargeteService, ec2.Port.tcp(3306));
    
    new cdk.CfnOutput(this, "URL", {
      value: lb.loadBalancerDnsName,
    })
  }
}

