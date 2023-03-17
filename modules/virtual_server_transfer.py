import paramiko

def transfer_configuration_file(host: str, user: str, password: str, content: str) -> str:
    '''
    Отправка конфигурационного файла серверу

    :param host - имя хоста сервера, либо его IP адрес:
    :param user - имя пользователя (учётные данные пользователя):
    :param password - пароль пользователя (учётные данные пользователя):
    :param content - содержимое для файла с конфигурацией:
    :return:
    '''

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=user, password=password)
    except:
        raise Exception("Невозможно подключиться к серверу по введённым данным")

    # Getting env variable for RabbitMQ configuration file if exists
    stdin, stdout, stderr = client.exec_command('printenv RABBITMQ_CONFIG_FILE')
    config_file = stdout.readline()

    if (config_file == ""):
        config_file = "/etc/rabbitmq/rabbitmq.conf"

    stdin, stdout, stderr = client.exec_command(f'echo \'{content}\' > {config_file}')

    # restarting the rabbitmq-server
    stdin, stdout, stderr = client.exec_command('sudo -S systemctl stop rabbitmq-server')
    stdin.write(password + "\n")
    stdin.flush()

    stdin, stdout, stderr = client.exec_command('sudo -S systemctl start rabbitmq-server')
    stdin.write(password + "\n")
    stdin.flush()

    return f"Конфигурационный файл на сервере: {host} создан по пути {config_file}"


def transfer_example_reciever(host: str, user: str, password: str, port: int = 5672, path: str = '/etc/rabbitmq'):
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

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=user, password=password)
    except:
        raise Exception("Невозможно подключиться к серверу по введённым данным")

    stdin, stdout, stderr = client.exec_command(f'echo -e \'{python_script}\' > {path}/reciever.py')

    return f"Для запуска получателя введите в терминале: python {path}/reciever.py"


def transfer_example_sender(host: str, user: str, password: str, port: int = 5672, path: str = '/etc/rabbitmq'):
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

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, username=user, password=password)
    except:
        raise Exception("Невозможно подключиться к серверу по введённым данным")

    stdin, stdout, stderr = client.exec_command(f'echo -e \'{python_script}\' > {path}/sender.py')

    return f"Для запуска отправителя введите в терминале: python {path}/sender.py"