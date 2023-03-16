import dataclasses
import json

from django.conf import settings
from httpx import Client

from .const import api_vk_get_long_poll_server_url
from .keyboards.main_menu import key_board_manager
from .types import MessageTypes


@dataclasses.dataclass
class LongPollApiParamsDto:
    key: str
    server: str
    ts: str


class VkManager:
    def __init__(self, access_token: str, group_id: str, vk_api_version: str) -> None:
        self.access_token: str = access_token
        self.group_id: str = group_id
        self.vk_api_version: str = vk_api_version
        self.key: str | None = None

    def get_long_poll_server(self) -> LongPollApiParamsDto:
        client = Client()
        form_data = {'access_token': self.access_token, 'group_id': self.group_id, 'v': self.vk_api_version}
        long_poll_server_params = client.post(url=api_vk_get_long_poll_server_url, data=form_data)
        return LongPollApiParamsDto(**long_poll_server_params.json()['response'])

    def send_message(self, user_id: int, keyboard: dict, message: str, attachment: str | None = None):
        # TODO переделать на Session
        client = Client()
        form_data = {
            'access_token': self.access_token,
            'group_id': self.group_id,
            'user_id': user_id,
            'message': message,
            'attachment': attachment,
            'keyboard': json.dumps(keyboard),
            'v': self.vk_api_version,
            'random_id': 0,
        }
        client.get('https://api.vk.com/method/messages.send/?' + self.query_build_params(form_data))

    @staticmethod
    def query_build_params(params: dict[str, str | int]) -> str:
        query_params = ""
        query_params += "&".join([f"{k}={v}" for k, v in params.items()])

        return query_params


class Dispatcher:
    def __init__(self, vk_manager: VkManager):
        self.vk_manager = vk_manager
        self.menu = key_board_manager.build_keyboard()

    def process_message(self, updates: dict) -> None:
        self.check_updates_keyboard()
        for update in updates:
            if update['type'] == MessageTypes.NEW_MESSAGE:
                user_id = update['object']['message']['from_id']
                payload = json.loads(update['object']['message']['payload'])
                next_level = payload['next_level']
                message = self.get_payload_message(payload)
                photo_link = self.get_payload_attachment(payload)
                self.vk_manager.send_message(user_id, self.menu[next_level], message, photo_link)

    def get_payload_message(self, payload: dict) -> str:
        return payload.get("message") or "Ошибка"

    def get_payload_attachment(self, payload: dict) -> str | None:
        return payload.get("photo_link")

    def check_updates_keyboard(self) -> None:
        with open(settings.KEYBOARD_STATUS_FILE_PATH, 'r+') as file:
            config = json.load(file)
            if not config["status"]:
                self.menu = key_board_manager.rebuild_keboard()
                config["status"] = True
            file.seek(0)
            file.truncate()
            json.dump(config, file, indent=2)


class Poller:
    def __init__(self, key: str, server: str, ts: str) -> None:
        self.is_running = False
        self.key: str = key
        self.server = server
        self.ts: str = ts
        self.wait: int = 10

    def start(self, dispatcher: Dispatcher) -> None:
        self.is_running = True
        self.poll(dispatcher)

    def stop(self) -> None:
        self.is_running = False

    def poll(self, dispatcher: Dispatcher):
        client = Client()
        while self.is_running:
            # TODO обработать протухание key
            response = client.get(f'{self.server}?key={self.key}&ts={self.ts}&wait={self.wait}&act=a_check', timeout=11)
            self.ts = response.json()["ts"]
            dispatcher.process_message(response.json()["updates"])
