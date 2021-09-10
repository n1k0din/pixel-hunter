from sqlalchemy import Column, MetaData, Table, VARCHAR, JSON

meta = MetaData()

image_color = Table(
    'image_color',
    meta,
    Column('id', VARCHAR, primary_key=True),
    Column('colors', JSON),
)
