#!/usr/bin/env python

import os

basedir = "/tmp"

class Config(object):
    SECRET_KEY = os.environ.get("SPOILER_SECRET_KEY") or "THIS IS A SECRET KEY"

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SPOILER_DEV_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "dev.db")
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SPOILER_PROD_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "prod.db")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SPOILER_TEST_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "test.db")
    TESTING = True

config = {
    "default": DevelopmentConfig,

    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
