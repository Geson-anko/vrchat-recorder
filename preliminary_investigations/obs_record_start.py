import obsws_python as obs
import time
import os
import pprint

host = "localhost"
port = 4444
password = "XfPnKZTkY1FgaISS"

cl = obs.ReqClient(host=host, port=port, password=password)

pprint.pprint(cl.get_output_list().outputs)
# cl.start_replay_buffer()
# cl.start_record()

# time.sleep(1)

# out = cl.stop_record()
# print(out.output_path)
# cl.stop_replay_buffer()