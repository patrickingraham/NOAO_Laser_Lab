
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException, ModbusIOException

UNIT = 0x1
print(f'UNIT is {UNIT}')

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Status request
status = [0, 0, 0, 0, 0, 13, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2] # length = 19
status_array = bytearray(status)
def run_sync_client():
    # Connect
    client = ModbusClient('192.168.0.148', 502)
    client.connect()
    client.set_debug(True)
    assert client.is_socket_open()

    log.debug("Write to multiple holding registers and read back")
    client.send(status_array)
    res = client.recv(24)
    log.debug(f'Got response of {list(res)}')

    #Appears that standard coils aren't supported
    # print('Writing Coil')
    # client.write_coil(1, True)
    # result = client.read_coils(1, 1)
    # print(f'result is {result}')
    # print(result.bits[0])
    import pdb;
    pdb.set_trace()
    rq = client.write_registers(1, status, unit=UNIT) # gives illegal address
    log.debug(f'status_array is {status_array}')
    # rq = client.write_registers(0, status_array, unit=UNIT) # gives illegal address
    # #rq = client.write_registers(2, status, unit=UNIT) # gives illegal address
    # #rq = client.write_registers(1, status) # also gives illegal address
    # #rq = client.write_registers(0, status) # also gives illegal address
    # #rq = client.write_registers(1, [0]*1, unit=UNIT) # also gives illegal address
    # #rq = client.write_registers(0, [0]*1, unit=UNIT) # also gives illegal address
    # #rq = client.write_registers(0, [0]*1) # also gives illegal address
    log.debug(f'rq is {rq}')

    # log.debug("Reading Coils")
    # # rr = client.read_coils(1, 1, unit=UNIT) # illegal address
    # rr = client.read_coils(0, 1, unit=UNIT) # illegal address
    # log.debug(rr)

    # client.send(status_array)
    # #rr = client.read_coils(1, 8, unit=UNIT) # no response
    # #rr = client.read_coils(0, 8, unit=UNIT) # no response
    # rr = client.read_coils(0, 8, unit=1) # no response
    # print(rr)

    #rr = client.read_input_registers(0, 23, unit=1)
    #rr = client.read_input_registers(1, 23, unit=1) # always get noResponse
    #
    # if rr.isError:
    # #    print(f'Error? {rr.isError()} Code:{rr.exception_code}')
    #     print(rr)

    #
    #
    #     ; print(f'Error? {rq.isError()} Code:{rq.exception_code}')
    #
    # print("Write to multiple holding registers and read back")
    # client.send(status_array)
    # res = client.recv(24)
    # print(res)
    #
    # client.send(status_array)
    # rr = client.read_holding_registers(23,unit=1) ; print(f'Error? {rr.isError()} Code:{rr.exception_code}')
    #
    #
    #
    # rq = client.write_registers(1, status, unit=1) ; print(f'Error? {rq.isError()} Code:{rq.exception_code}')
    #
    # arguments = {
    #     'read_address': 1,
    #     'read_count': 23,
    #     'write_address': 1,
    #     'write_registers': status,
    # }
    # log.debug("Read write registeres simulataneously")
    # rq = client.readwrite_registers(unit=UNIT, **arguments)
    # rr = client.read_holding_registers(1, 8, unit=UNIT)
    # assert (not rq.isError())  # test that we are not an error
    # assert (rq.registers == [20] * 8)  # test the expected value
    # assert (rr.registers == [20] * 8)  # test the expected value
    #
    #
    #
    # rq = client.write_registers(1, status)
    # try:
    #     assert (not rq.isError())  # test that we are not an error
    # except AssertionError:
    #     print(f'Writing Error code is {rq.exception_code}')
    #
    #
    # rr = client.read_holding_registers(0, len(status))
    #
    # assert (rr.registers == [10] * 8)  # test the expected value
    #
    #
    # write_test = client.write_registers(1, status)
    # write_test.isError()
    #
    # read_test = client.read_registers(1,)
    # # response from sending status array via igus code
    # #res = [0, 0, 0, 0, 0, 15, 0, 43, 13, 0, 0, 0, 96, 65, 0, 0, 0, 0, 2, 8, 4]
    #
    # # read input should be address 0
    # # write input should be address 1?
    #
if __name__ == "__main__":
    run_sync_client()