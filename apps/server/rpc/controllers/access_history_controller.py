import datetime
import typing

from apps.server.database import InsertMain, SelectMain
from apps.server.security import Security
from libs import LogMaker
from packages.errors.errors import *
from packages.responses.responses import *
from packages.schemas.session_header import SessionHeader


class AccessHistoryController:
    @staticmethod
    def create_access_history(payload: typing.Dict[str, typing.Any]):
        print(f"PAY {payload}")
        try:
            InsertMain.insert_access_history(payload)
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_user_access_history(header: typing.Dict[str, typing.Any], user_id: str):
        try:
            # date_ini: str | None, date_end: str | None
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            if not user_id:
                return BadRequestError("ID do usuário não informado").dict()

            data = SelectMain.select_user_access_history(user_id)
            response = []
            if data:
                for d in data:
                    admin = SelectMain.select_admin_by_id(str(d.admin_id))
                    user = SelectMain.select_user_by_id(str(d.user_id))
                    device = SelectMain.select_device_by_id(str(d.device_id))
                    response.append(
                        {
                            "id": str(d.id),
                            "user_id": str(user.id),
                            "user_name": user.name,
                            "admin_id": str(admin.id),
                            "admin_name": admin.name,
                            "device_id": str(device.id),
                            "device_name": device.name,
                            "when": d.created_at,
                        }
                    )
                return OKResponse(
                    message="Histórico de acessos encontrado com sucesso", data=response
                ).dict()
            return NoContentResponse(
                "Nenhum histórico de acesso encontrado para este usuário", data=[]
            ).dict()

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
        return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_device_access_history_by_date(
        header: typing.Dict[str, typing.Any], device_id: str, date: str
    ):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            if not device_id:
                return BadRequestError("ID do dispositivo não informado").dict()

            if not date:
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")

            data = SelectMain.select_device_access_history_by_date(device_id, date)
            response = []
            if data:
                for d in data:
                    if d.admin_id:
                        admin = SelectMain.select_admin_by_id(str(d.admin_id))

                    user = SelectMain.select_user_by_id(str(d.user_id))
                    device = SelectMain.select_device_by_id(str(d.device_id))
                    response.append(
                        {
                            "id": str(d.id),
                            "user_id": str(user.id),
                            "user_name": user.name,
                            "admin_id": str(admin.id) if d.admin_id else "",
                            "admin_name": admin.name if d.admin_id else "",
                            "device_id": str(device.id),
                            "device_name": device.name,
                            "when": d.created_at,
                        }
                    )
                return OKResponse(
                    message="Histórico de acessos encontrado com sucesso", data=response
                ).dict()
            return NoContentResponse(
                "Nenhum histórico de acesso encontrado para esta data", data=[]
            ).dict()

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
        return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_device_access_history(
        header: typing.Dict[str, typing.Any],
        device_id: str,
        date_ini: str | None,
        date_end: str | None,
    ):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            if not device_id:
                return BadRequestError("ID do dispositivo não informado").dict()

            if not date_ini and not date_end:
                today = datetime.datetime.now()
                start = datetime.datetime(today.year, today.month, today.day, 6, 0)
                date_ini = start.strftime("%Y-%m-%d %H:%M")
                date_end = today.strftime("%Y-%m-%d %H:%M")

            data = SelectMain.select_device_access_history(device_id, date_ini, date_end)
            response = []
            if data:
                for d in data:
                    admin = SelectMain.select_admin_by_id(str(d.admin_id))
                    user = SelectMain.select_user_by_id(str(d.user_id))
                    device = SelectMain.select_device_by_id(str(d.device_id))
                    response.append(
                        {
                            "id": str(d.id),
                            "user_id": str(user.id),
                            "user_name": user.name,
                            "admin_id": str(admin.id),
                            "admin_name": admin.name,
                            "device_id": str(device.id),
                            "device_name": device.name,
                            "when": d.created_at,
                        }
                    )
                return OKResponse(
                    message="Histórico de acessos encontrado com sucesso", data=response
                ).dict()
            return NoContentResponse(
                "Nenhum histórico de acesso encontrado para este dispositivo", data=[]
            ).dict()

        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
        return InternalServerError("Não foi possível processar a requisição").dict()
