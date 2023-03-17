from python_on_whales import docker

def transfer_configuration_file(container_name: str, content: str) -> str:
    '''
    Отправка файла с конфигурацией брокера в контейнер

    :param container_name - имя контейнера, где располагается брокер RabbitMQ:
    :param content - содержимое для файла с конфигурацией:
    :return:
    '''

    # Checking if it is possible to connect to container
    try:
        docker.execute(container=container_name,
                       command=['ls'])
    except:
        raise Exception("Невозможно найти запущенный контейнер по данному имени")

    try:
        data = docker.execute(container=container_name,
                              command=['/bin/sh', '-c', 'cd /etc/rabbitmq'])
    except:
        raise Exception("Брокер RabbitMQ не найден в контейнере")

    config_file = ""

    # Getting env variable for RabbitMQ configuration file if exists
    try:
        config_file = docker.execute(container=container_name,
                                     command=['/bin/sh', '-c', 'printenv RABBITMQ_CONFIG_FILE'])
    except:
        config_file = "/etc/rabbitmq/rabbitmq.conf"

    docker.execute(container=container_name,
                   command=['/bin/sh', '-c', f'echo \'{content}\' > {config_file}'])

    return f"Конфигурационный файл в контейнере: {container_name} создан по пути {config_file}"

def transfer_example_reciever(container_name: str, port: int = 5672, path: str = '/etc/rabbitmq'):
    '''
    Отправка простейшего примера получателя сообщений

    :param host - имя хоста сервера:
    :param user - имя пользователя на сервере:
    :param password = пароль пользователя:
    :param port - порт, на котором запущен брокер:
    :param path - желаемый путь, где будет располагаться .py файл:
    :return:
    '''

    python_script = "import pika, sys, os\n\n" \
                    "def main():\n    " \
                    "pika.BlockingConnection(pika.ConnectionParameters())\n    " \
                    "connection = pika.BlockingConnection(pika.ConnectionParameters(host=\"localhost\", port=" + str(port) + \
                    "))\n    " \
                    "channel = connection.channel()\n\n    " \
                    "channel.queue_declare(queue=\'hello\')\n\n    " \
                    "def callback(ch, method, properties, body):\n        " \
                    "print(\" [x] Received %r\" % body)\n\n    " \
                    "channel.basic_consume(queue=\"hello\", on_message_callback=callback, auto_ack=True)\n\n    " \
                    "print(\" [*] Waiting for messages. To exit press CTRL+C\")\n    " \
                    "channel.start_consuming()\n\n" \
                    "if __name__ == \'__main__\':\n    " \
                    "try:\n        " \
                    "main()\n    " \
                    "except KeyboardInterrupt:\n        " \
                    "print(\"Interrupted\")\n        " \
                    "try:\n            " \
                    "sys.exit(0)\n        " \
                    "except SystemExit:\n            " \
                    "os._exit(0)"

    try:
        docker.execute(container=container_name,
                       command=['ls'])
    except:
        raise Exception("Невозможно найти запущенный контейнер по данному имени")

    docker.execute(container=container_name,
                   command=['/bin/sh', '-c', f'echo \'{python_script}\' > {path}/reciever.py'])

    return f"Для запуска получателя в командной строке контейнера введите: python {path}/reciever.py"


def transfer_example_sender(container_name: str, port: int = 5672, path: str = '/etc/rabbitmq'):
    '''
    Отправка простейшего примера отправителя сообщений

    :param host - имя хоста сервера:
    :param user - имя пользователя на сервере:
    :param password = пароль пользователя:
    :param port - порт, на котором запущен брокер:
    :param path - желаемый путь, где будет располагаться .py файл:
    :return:
    '''

    python_script = "import pika\n\n" \
                    "connection = pika.BlockingConnection(pika.ConnectionParameters(host=\"localhost\", port=" + str(port) + \
                    "))\n\n" \
                    "channel = connection.channel()\n\n" \
                    "channel.queue_declare(queue=\"hello\")\n\n" \
                    "channel.basic_publish(exchange=\"\", routing_key=\"hello\", body=\"Example message\")\n" \
                    "print(\" [x] Sent \'Example message\'\")\n" \
                    "connection.close()"

    try:
        docker.execute(container=container_name,
                       command=['ls'])
    except:
        raise Exception("Невозможно найти запущенный контейнер по данному имени")

    docker.execute(container=container_name,
                   command=['/bin/sh', '-c', f'echo \'{python_script}\' > {path}/sender.py'])

    return f"Для запуска отправителя в командной строке контейнера введите: python {path}/sender.py"