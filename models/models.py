from dataclasses import dataclass
from typing import Any

@dataclass
class ServerModel:
    '''
    Модель сервера

    :param host_name - имя хоста сервера, либо его IP адрес:
    :param user_name - имя пользователя (учётные данные пользователя):
    :param password - пароль пользователя (учётные данные пользователя):
    '''

    host_name: str
    user_name: str
    password: str


@dataclass
class DockerModel:
    '''
    Модель контейнера

    :param container_name - имя хоста сервера, либо его IP адрес:
    '''

    container_name: str


@dataclass
class RabbitMQConfigurationOption:
    '''
    Модель отдельной опции для брокера RabbitMQ

    :param file_name - имя, которое указано  в конфигурационном файле:
    :param common_name - имя, которое понятно обычном пользователю:
    :param brief_description - описание того, за что отвечает данная опиця:
    :param value - значение опции:
    '''

    file_name: str
    common_name: str
    brief_description: str
    value: Any

