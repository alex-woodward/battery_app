# Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""A sample Velocitas vehicle app for adjusting seat position."""

import json
import logging

from vehicle import Vehicle  # type: ignore
from velocitas_sdk.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from velocitas_sdk.vehicle_app import VehicleApp, subscribe_topic

logging.setLogRecordFactory(get_opentelemetry_log_factory())
logging.basicConfig(format=get_opentelemetry_log_format())
logging.getLogger().setLevel("DEBUG")
logger = logging.getLogger(__name__)


class BatteryApp(VehicleApp):
    """
    Sample Connectivity

    The BatteryApp subscribes to MQTT topics to listen for incoming requests to
    get or set various battery-related parameters such as temperature, voltage,
    capacity, state of charge, and charging status. It interacts with the vehicle’s
    traction battery system to update these parameters as requested and publishes
    the current values of these parameters to specific MQTT topics.

    The app also listens for updates from the VehicleDataBroker on battery signals
    like temperature, cell voltage, and current, and publishes these updates
    to the relevant MQTT topics for external applications or monitoring systems.
    """

    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client

    async def on_start(self):
        pass

    # GETTERS #
    @subscribe_topic("batteryapp/temperature/getAverage")
    async def on_get_average_temperature_request_received(self, data: str) -> None:
        response_topic = "batteryapp/temperature/getAverage/response"

        average_temp = (
            await self.Vehicle.Powertrain.TractionBattery.Temperature.Average.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Average temperature = {average_temp}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/cell/getTemperature")
    async def on_get_cell_temperature_request_received(self, data_str: str) -> None:
        data = json.loads(data_str)
        response_topic = "batteryapp/cell/getTemperature/response"

        cell = data["cellPosition"]
        cellTemp = (
            await self.Vehicle.Powertrain.TractionBattery.Temperature.CellTemperature.get()
        ).value[cell]

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Cell {cell} temperature = {cellTemp}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/cell/getVoltage")
    async def on_get_cell_voltage_request_received(self, data_str: str) -> None:
        data = json.loads(data_str)
        response_topic = "batteryapp/cell/getVoltage/response"

        cell = data["cellPosition"]
        cellVoltage = (
            await self.Vehicle.Powertrain.TractionBattery.CellVoltage.CellVoltages.get()
        ).value[cell]

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Cell {cell} voltage = {cellVoltage}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/getGrossCapacity")
    async def on_get_gross_capacity_request_received(self, data_str: str) -> None:
        response_topic = "batteryapp/getGrossCapacity/response"

        gross_capacity = (
            await self.Vehicle.Powertrain.TractionBattery.GrossCapacity.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Gross capacity: {gross_capacity}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/getNetCapacity")
    async def on_get_net_capacity_request_received(self, data_str: str) -> None:
        response_topic = "batteryapp/getNetCapacity/response"

        net_capacity = (
            await self.Vehicle.Powertrain.TractionBattery.NetCapacity.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Net capacity: {net_capacity}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/stateOfCharge/getDisplayed")
    async def on_get_state_of_charge_displayed_request_received(
        self, data_str: str
    ) -> None:
        response_topic = "batteryapp/stateOfCharge/getDisplayed/response"

        state_of_charge = (
            await self.Vehicle.Powertrain.TractionBattery.StateOfCharge.Displayed.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Displayed state of charge: {state_of_charge}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/getCurrentVoltage")
    async def on_get_current_voltage_request_received(self, data_str: str) -> None:
        response_topic = "batteryapp/getCurrentVoltage/response"

        current_voltage = (
            await self.Vehicle.Powertrain.TractionBattery.CurrentVoltage.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Current voltage: {current_voltage}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/getCurrentCurrent")
    async def on_get_current_current_request_received(self, data_str: str) -> None:
        response_topic = "batteryapp/getCurrentCurrent/response"

        current_current = (
            await self.Vehicle.Powertrain.TractionBattery.CurrentCurrent.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Current current: {current_current}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/charging/getIsCharging")
    async def on_get_is_charging_request_received(self, data_str: str) -> None:
        response_topic = "batteryapp/charging/getIsCharging/response"

        is_charging = (
            await self.Vehicle.Powertrain.TractionBattery.Charging.IsCharging.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Is charging: {is_charging}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/cell/getIsCharging")
    async def on_get_cell_is_charging_request_received(self, data_str: str) -> None:
        data = json.loads(data_str)
        response_topic = "batteryapp/cell/getIsCharging/response"

        cell = data["cellPosition"]
        cell_is_charging = (
            await self.Vehicle.Powertrain.TractionBattery.Charging.CellIsCharging.get()
        ).value[cell]

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Cell {cell} is charging: {cell_is_charging}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/charging/getIsDischarging")
    async def on_get_is_discharging_request_received(self, data_str: str) -> None:
        response_topic = "batteryapp/charging/getIsDischarging/response"

        is_discharging = (
            await self.Vehicle.Powertrain.TractionBattery.Charging.IsDischarging.get()
        ).value

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Is discharging: {is_discharging}""",
                    },
                }
            ),
        )

    @subscribe_topic("batteryapp/cell/getIsDischarging")
    async def on_get_cell_is_discharging_request_received(self, data_str: str) -> None:
        data = json.loads(data_str)
        response_topic = "batteryapp/cell/getIsDischarging/response"

        cell = data["cellPosition"]
        cell_is_discharging = (
            await self.Vehicle.Powertrain.TractionBattery.Charging.CellIsDischarging.get()
        ).value[cell]

        await self.publish_event(
            response_topic,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Cell {cell} is discharging: {cell_is_discharging}""",
                    },
                }
            ),
        )

    # COMMANDS #
    @subscribe_topic("batteryapp/charging/setIsCharging")
    async def on_set_is_charging_request_received(self, data_str: str) -> None:
        data = json.loads(data_str)
        response_topic = "batteryapp/charging/setIsCharging/response"
        response_data = {"requestId": data["requestId"], "result": {}}

        state = data["state"]
        is_discharging = (
            await self.Vehicle.Powertrain.TractionBattery.Charging.IsDischarging.get()
        ).value

        if not is_discharging:
            try:
                await self.Vehicle.Powertrain.TractionBattery.Charging.IsCharging.set(
                    state
                )
                response_data["result"] = {
                    "status": 0,
                    "message": f"Set charging state to: {state}",
                }
            except ValueError as error:
                response_data["result"] = {
                    "status": 1,
                    "message": f"Failed to set charging state to {state}, error: {error}",
                }
            except Exception:
                response_data["result"] = {
                    "status": 1,
                    "message": "Exception on set charging state",
                }
        else:
            error_msg = f"""Not allowed to change charging state because discharging state is {is_discharging} and not false"""
            response_data["result"] = {"status": 1, "message": error_msg}

        await self.publish_event(response_topic, json.dumps(response_data))

    @subscribe_topic("batteryapp/charging/setIsDischarging")
    async def on_set_is_discharging_request_received(self, data_str: str) -> None:
        data = json.loads(data_str)
        response_topic = "batteryapp/charging/setIsDischarging/response"
        response_data = {"requestId": data["requestId"], "result": {}}

        state = data["state"]
        is_charging = (
            await self.Vehicle.Powertrain.TractionBattery.Charging.IsCharging.get()
        ).value

        if not is_charging:
            try:
                await (
                    self.Vehicle.Powertrain.TractionBattery.Charging.IsDischarging.set(
                        state
                    )
                )
                response_data["result"] = {
                    "status": 0,
                    "message": f"Set discharging state to: {state}",
                }
            except ValueError as error:
                response_data["result"] = {
                    "status": 1,
                    "message": f"Failed to set discharging state to {state}, error: {error}",
                }
            except Exception:
                response_data["result"] = {
                    "status": 1,
                    "message": "Exception on set discharging state",
                }
        else:
            error_msg = f"""Not allowed to change discharging state because charging state is {is_charging} and not false"""
            response_data["result"] = {"status": 1, "message": error_msg}

        await self.publish_event(response_topic, json.dumps(response_data))
