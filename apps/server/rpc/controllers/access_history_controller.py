import datetime
import typing

from apps.server.database import InsertMain, SelectMain
from apps.server.database.models.__all_models import *
from apps.server.security import Security
from libs import LogMaker
from packages.errors.errors import *
from packages.responses.responses import *
from packages.schemas.devices_schema import DeviceSchema
from packages.schemas.session_header import SessionHeader


class AccessHistoryController:
    @staticmethod
    def create_access_history(payload: typing.Dict[str, typing.Any]):
        # We won't use that method in api requests
        try:
            pass
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_access_history(
        header: typing.Dict[str, typing.Any], date_ini: str | None, date_end: str | None
    ):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            if not date_ini or not date_end:
                today = datetime.datetime.now()
                start = datetime.datetime(today.year, today.month, today.day, 6, 0)
                date_ini = start.strftime("%Y-%m-%d %H:%M")
                date_end = today.strftime("%Y-%m-%d %H:%M")

            data = SelectMain.select_access_history(date_ini, date_end)
            response = []
            if data:
                for d in data:
                    user = SelectMain.select_user_by_id(str(d.user_id))
                    member = SelectMain.select_member_by_id(str(d.member_id))
                    device = SelectMain.select_device_by_id(str(d.device_id))
                    response.append(
                        {
                            "id": str(d.id),
                            "member_id": str(member.id),
                            "member_name": member.name,
                            "user_id": str(user.id),
                            "user_name": user.name,
                            "device_id": str(device.id),
                            "device_name": device.name,
                            "when": d.created_at,
                        }
                    )
                return OKResponse(
                    message=f"Histórico de acessos de {date_ini} até {date_end} encontrado com sucesso",
                    data=response,
                ).dict()
            return NoContentResponse(
                f"Nenhum histórico de acesso encontrado de {date_ini} até {date_end}"
            ).dict()

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
        return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_all_access_history(header: typing.Dict[str, typing.Any]):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = SelectMain.select_all_access_history()
            response = []
            if data:
                for d in data:
                    user = SelectMain.select_user_by_id(str(d.user_id))
                    member = SelectMain.select_member_by_id(str(d.member_id))
                    device = SelectMain.select_device_by_id(str(d.device_id))
                    response.append(
                        {
                            "id": str(d.id),
                            "member_id": str(member.id),
                            "member_name": member.name,
                            "user_id": str(user.id),
                            "user_name": user.name,
                            "device_id": str(device.id),
                            "device_name": device.name,
                            "when": d.created_at,
                        }
                    )
                return OKResponse(
                    message="Histórico de acessos encontrado com sucesso", data=response
                ).dict()
            return NoContentResponse("Nenhum histórico de acesso encontrado").dict()

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
        return InternalServerError("Não foi possível processar a requisição").dict()
