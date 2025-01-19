import logging
import os
import sys
import yaml


class AppConfig:
    """Class to hold the application configuration."""
    def __init__(self):
        """Initializes the AppConfig class."""
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
        self.ZEPHYR_SERVICE_URL = os.getenv('ZEPHYR_SERVICE_URL', '')
        self.validate()

    def validate(self):
        """Validates the configuration."""
        if self.LOG_LEVEL not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            raise ValueError(f"Invalid LOG_LEVEL: {self.LOG_LEVEL}")


class FlaskConfig:
    """Class to hold the Flask configuration."""
    def __init__(self):
        self.FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
        self.FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
        self.FLASK_PORT = os.getenv('FLASK_PORT', '8080')
        self.validate()

    def validate(self):
        if not isinstance(self.FLASK_DEBUG, bool):
            raise ValueError(f"Invalid FLASK_DEBUG: {self.FLASK_DEBUG}")


class OtelConfig:
    """Class to hold the OpenTelemetry configuration."""
    def __init__(self):
        self.JAEGER_HOST = os.getenv('JAEGER_HOST', '0.0.0.0')
        self.JAEGER_PORT = os.getenv('JAEGER_PORT', '6831')
        self.validate()

    def validate(self):
        pass


class TemporalConfig:
    """Class to hold Temporal configs"""
    def __init__(self):
        self.TEMPORAL_SERVER_HOST = os.getenv('TEMPORAL_SERVER_HOST', 'localhost')
        self.TEMPORAL_SERVER_PORT = os.getenv('TEMPORAL_SERVER_PORT', '7233')
        self.TEMPORAL_NAMESPACE = os.getenv('TEMPORAL_NAMESPACE', 'default')
        self.TEMPORAL_TLS_ENABLED = os.getenv('TEMPORAL_TLS_ENABLED', 'False').lower() in ['true', '1', 'yes']
        self.validate()

    def validate(self):
        if not self.TEMPORAL_SERVER_HOST:
            raise ValueError("TEMPORAL_SERVER_HOST is required")
        if not self.TEMPORAL_SERVER_PORT:
            raise ValueError("TEMPORAL_SERVER_PORT is required")
        if not self.TEMPORAL_NAMESPACE:
            raise ValueError("TEMPORAL_NAMESPACE is required")


class TemporalWorkflowConfig:
    """Class to hold the Temporal workflow configuration."""
    def __init__(self):
        self.config_file = os.getenv('TEMPORAL_WORKFLOW_CONFIG')
        self.validate()
        self.workflows = self.load_workflows()

    def validate(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Workflow configuration file not found: {self.config_file}")

    def load_workflows(self):
        with open(self.config_file, 'r') as file:
            workflows = yaml.safe_load(file)
        return workflows

    def get_workflow_config(self, workflow_name):
        if workflow_name in self.workflows:
            return self.workflows[workflow_name]
        else:
            raise ValueError(f"Workflow configuration for {workflow_name} not found")


class CloudConfig:
    """Class to hold the Cloud configuration."""
    def __init__(self):
        self.config_file = os.getenv('CLOUD_CONFIG')
        self.validate()
        self.workflows = self.load_workflows()

    def validate(self):
        if self.config_file == "" or self.config_file is None:      # preventive measure
            return
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Workflow configuration file not found: {self.config_file}")

    def load_workflows(self):
        if self.config_file == "" or self.config_file is None:      # preventive measure
            return {}
        with open(self.config_file, 'r') as file:
            workflows = yaml.safe_load(file)
        return workflows

    def get_cloud_config(self, block_name):
        if block_name in self.workflows:
            return self.workflows[block_name]
        else:
            raise ValueError(f"Workflow configuration for {block_name} not found")


class Config:
    """Class to hold the entire application configuration."""
    def __init__(self):
        self.app_config = AppConfig()
        self.temporal_config = TemporalConfig()
        self.temporal_workflow_config = TemporalWorkflowConfig()
        self.flask_config = FlaskConfig()
        self.headers = dict()

    def log_config(self):
        _attr = (
            f"App Configuration:\n"
            f"LOG_LEVEL: {self.app_config.LOG_LEVEL}\n"
        )
        _attr += (
            f"\nFlask Configuration:\n"
            f"FLASK_DEBUG: {self.flask_config.FLASK_DEBUG}\n"
            f"FLASK_HOST: {self.flask_config.FLASK_HOST}\n"
            f"FLASK_PORT: {self.flask_config.FLASK_PORT}\n"
            f"\nTemporal Configuration:\n"
            f"TEMPORAL_SERVER_HOST: {self.temporal_config.TEMPORAL_SERVER_HOST}\n"
            f"TEMPORAL_SERVER_PORT: {self.temporal_config.TEMPORAL_SERVER_PORT}\n"
            f"TEMPORAL_NAMESPACE: {self.temporal_config.TEMPORAL_NAMESPACE}\n"
            f"TEMPORAL_TLS_ENABLED: {self.temporal_config.TEMPORAL_TLS_ENABLED}\n"
            f"\nTemporal Workflow Configuration:\n"
            f"TEMPORAL_WORKFLOW_CONFIG: {self.temporal_workflow_config.config_file}\n"
        )
        print(_attr)


config = Config()
config.log_config()
