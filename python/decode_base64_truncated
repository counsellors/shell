# encoding: utf-8

import base64

def decode_base64_truncated(encoded_str):
	for i in range(len(encoded_str)):
		truncated_str = encoded_str[:i+1]
		try:
			decoded_bytes = base64.b64decode(truncated_str)
			decoded_str = decoded_bytes.decode('utf-8')
			print(decoded_str)
		except:
			pass

if __name__ == "__main__":
	encoded_str = "SGVsbG8gV29ybGQhISEhCg=="
	decode_base64_truncated(encoded_str)

