"""
Copyright 2016 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from sqlalchemy import Table, Column, MetaData, ForeignKey, Index
from sqlalchemy import Integer, String, Text

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


metadata = MetaData()


projects_table = Table(
    'projects', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('name', String(256), nullable=False)
)

suites_table = Table(
    'suites', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('project_id', ForeignKey(projects_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('name', String(256), nullable=False),
    Column('description', String(256), nullable=True),

    Index('suite_index', 'project_id', 'id')
)

builds_table = Table(
    'builds', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('project_id', ForeignKey(projects_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('suite_id', ForeignKey(suites_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('build_num', Integer, nullable=False),
    Column('timestamp', Integer, nullable=False),

    Index('build_index', 'project_id', 'suite_id', 'build_num')
)

results_table = Table(
    'results', metadata,
    Column('id', Integer, nullable=False, primary_key=True,
           autoincrement=True),
    Column('project_id', ForeignKey(projects_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('suite_id', ForeignKey(suites_table.c.id, ondelete='CASCADE'),
           nullable=False),
    Column('build_num', Integer, nullable=False),
    Column('test_name', String(256), nullable=False),
    Column('timestamp', Integer, nullable=False),
    Column('result', String(256), nullable=False),
    Column('result_message', Text, nullable=True),
    Column('region', String(256), nullable=True),
    Column('environment', String(256), nullable=True),
    Column('build_url', String(256), nullable=True),
    Column('extra_data', String(512), nullable=True),

    Index('result_index', 'project_id', 'suite_id', 'build_num', 'result')
)


def db_connect(database_dict):
    engine = create_engine(URL(**database_dict))
    metadata.create_all(engine)
    return engine