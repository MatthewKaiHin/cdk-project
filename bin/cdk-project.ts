#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { CdkProjectStack } from '../lib/cdk-project-stack';

const app = new cdk.App();
new CdkProjectStack(app, 'CdkProjectStack');
