import modules.virtual_server_transfer as vst
import modules.docker_transfer as dt

'''
Пример отправки конфигурационного файла и тестового примера на сервер


vst.transfer_configuration_file(host="localhost", user="guest", password="123", content="Some content here")
vst.transfer_example_reciever(host="localhost", user="guest", password="123")
vst.transfer_example_sender(host="localhost", user="guest", password="123")
'''

'''
Пример отправки конфигурационного файла и тестового примера в контейнер


dt.transfer_configuration_file(container_name="some-name", content="Some content here")
dt.transfer_example_reciever(container_name="some-name")
dt.transfer_example_sender(container_name="some-name")
'''
