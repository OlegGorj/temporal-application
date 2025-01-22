import uuid
from types import NoneType
from typing import Any, Optional
import logging

import asyncio

from flask import request
from flask_restx import Namespace, Resource
from flask_restx import reqparse
from marshmallow.exceptions import MarshmallowError

from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from appcode_onboard_service.shared.common import ServiceTiersShort, LoggerFactory
from appcode_onboard_service.config import config
from temporal_shared.common.headers import Headers
from temporal_shared.models import AppcodeOnboardRequestSchema, AppCode
from appcode_onboard_service.api.temporal_manager import async_engage_temporal_workflow, start_temporal_workflow_execution, query_temporal_workflow_execution_status


api = Namespace('AppCode Onboard', description='AppCode Onboard operations')
api_health = Namespace('Health', description='Service health')

logging.basicConfig(level=logging.DEBUG)




class AppCodeController:
    """Controller class for AppCode Onboard API.
    """
    LOG = LoggerFactory.get_logger(__name__, __qualname__)

    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="AppCodeOnboardExecutor")

    def post_appcode_onboard(self, appcode: str, headers: dict = None):
        # basic validation of parameters
        if appcode is None:
            return self._render_response("", "", "Must provide App Code"), 400

        try:
            _AppcodeRequest = AppcodeOnboardRequestSchema().load(request.get_json())  # parse incoming request
        except MarshmallowError as e:
            message = "Failed to deserialize request body."
            self.LOG.exception(message)
            return self._render_response(None, None, "MarshmallowError: " + e.args[0]), 400
        except TypeError as e:
            message = "TypeError: Failed to deserialize request body."
            self.LOG.exception(message)
            return self._render_response(None, None, "TypeError: " + e.args[0]), 400
        
        _workflow_config = config.temporal_workflow_config.get_workflow_config("appcode_onboard")
        if _workflow_config is None:
            return self._render_response("", "", "Failed to get workflow config"), 400

        # set all necessary parameters
        _appcode = appcode.lower()
        _service_tier = _AppcodeRequest.service_tier.lower()
        _workflow_request_object = AppCode(appcode=_appcode, request=_AppcodeRequest, id=None)
        _solution_id = str(_AppcodeRequest.solutions[0]).lower()  # get solution ID
        _workflow_id = f"{appcode.upper()}::{_service_tier.upper()}::AppCodeOnboard"

        # submit temporal request to async execute workflow described by _workflow_config
        # try:
        future = self._executor.submit(
            asyncio.run,
            start_temporal_workflow_execution(
                appcode=_appcode,
                service_tier=_service_tier,
                workflow_payload_request=_workflow_request_object,
                headers=headers,
            )
        )
        _wf_result = future.result()
        self.LOG.info(f"Spawned workflow with workflow ID {_workflow_id}, intermediate workflow result: {_wf_result}")
        return self._render_response(_appcode, _solution_id), 201
    