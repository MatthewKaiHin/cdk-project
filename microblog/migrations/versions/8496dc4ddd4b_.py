"""empty message

Revision ID: 8496dc4ddd4b
Revises: 
Create Date: 2020-05-02 15:50:02.522047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8496dc4ddd4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('banner', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('categories', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_categories'), 'categories', ['categories'], unique=True)
    op.create_table('company_brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('companybrand', sa.String(length=50), nullable=True),
    sa.Column('photourl', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_brand_companybrand'), 'company_brand', ['companybrand'], unique=True)
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feature_timestamp'), 'feature', ['timestamp'], unique=False)
    op.create_table('product_brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productbrand', sa.String(length=500), nullable=True),
    sa.Column('imgurl', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_brand_productbrand'), 'product_brand', ['productbrand'], unique=True)
    op.create_table('promotion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=True),
    sa.Column('endpoint', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_region_region'), 'region', ['region'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('district',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('district', sa.String(length=50), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_district_district'), 'district', ['district'], unique=True)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('sub_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subcategories', sa.String(length=500), nullable=True),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categories_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sub_categories_subcategories'), 'sub_categories', ['subcategories'], unique=True)
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product', sa.String(length=500), nullable=True),
    sa.Column('volumn', sa.String(length=500), nullable=True),
    sa.Column('price', sa.String(length=500), nullable=True),
    sa.Column('pricedown', sa.String(length=500), nullable=True),
    sa.Column('details', sa.String(length=500), nullable=True),
    sa.Column('origin', sa.String(length=500), nullable=True),
    sa.Column('productimage', sa.String(length=500), nullable=True),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.Column('productbrand_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categories_id'], ['sub_categories.id'], ),
    sa.ForeignKeyConstraint(['productbrand_id'], ['product_brand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('store', sa.String(length=500), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('tel', sa.String(length=500), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('companybrand_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['companybrand_id'], ['company_brand.id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_store_store'), 'store', ['store'], unique=True)
    op.create_index(op.f('ix_store_timestamp'), 'store', ['timestamp'], unique=False)
    op.create_table('promotion_products',
    sa.Column('promotion_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotion.id'], )
    )
    op.create_index('promo_items', 'promotion_products', ['promotion_id', 'product_id'], unique=True)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating1', sa.Float(), nullable=True),
    sa.Column('rating2', sa.Float(), nullable=True),
    sa.Column('rating3', sa.Float(), nullable=True),
    sa.Column('rating4', sa.Float(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_timestamp'), 'review', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_review_timestamp'), table_name='review')
    op.drop_table('review')
    op.drop_index('promo_items', table_name='promotion_products')
    op.drop_table('promotion_products')
    op.drop_index(op.f('ix_store_timestamp'), table_name='store')
    op.drop_index(op.f('ix_store_store'), table_name='store')
    op.drop_table('store')
    op.drop_table('product')
    op.drop_index(op.f('ix_sub_categories_subcategories'), table_name='sub_categories')
    op.drop_table('sub_categories')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('followers')
    op.drop_index(op.f('ix_district_district'), table_name='district')
    op.drop_table('district')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_region_region'), table_name='region')
    op.drop_table('region')
    op.drop_table('promotion')
    op.drop_index(op.f('ix_product_brand_productbrand'), table_name='product_brand')
    op.drop_table('product_brand')
    op.drop_index(op.f('ix_feature_timestamp'), table_name='feature')
    op.drop_table('feature')
    op.drop_index(op.f('ix_company_brand_companybrand'), table_name='company_brand')
    op.drop_table('company_brand')
    op.drop_index(op.f('ix_categories_categories'), table_name='categories')
    op.drop_table('categories')
    op.drop_table('banner')
    # ### end Alembic commands ###