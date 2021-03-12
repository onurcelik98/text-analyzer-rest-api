from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import text_analyzer


# Opening the json database
with open("db.json", encoding='utf8') as data_file:
	data = json.load(data_file)
	for entry in data:
		data[entry].encode('utf8')


# A very basic HTTP request Handler class that can only perform GET and POST
class RequestHandler(BaseHTTPRequestHandler):
	def _set_headers(self):  # Sets basic headers
		self.send_response(201, "Created")
		self.send_header('Content-type', 'text/json')
		length = int(self.headers['Content-Length'])
		content = self.rfile.read(length).decode("utf-8")  # using UTF-8 to be able to process Turkish letters
		temp = str(content)
		self.end_headers()
		return temp

	# Method definitions
	def do_GET(self):  # GET method
		self.send_response(200, "OK")
		self.send_header('Content-type', 'text/json')
		self.end_headers()
		self.wfile.write((json.dumps(data, indent=4, ensure_ascii=False) + "\n").encode())

	def do_POST(self):  # POST method
		# Appending the new content to the end
		content = self._set_headers()
		key = 0
		for (key, value) in data.items():
			pass
		index = int(key) + 1
		data[str(index)] = str(content)
		# Writing to the json file
		with open("db.json", 'w+', encoding='utf8') as file_data:
			json.dump(data, file_data, ensure_ascii=False)
		try:
			# Constructing a TextAnalyzer class instance out of the data to analyze
			input_object = data[str(index)]
			input_dict = json.loads(input_object, strict=False)
			input_string = input_dict["text"]
			input_filters = None
			if "analysis" in input_dict:
				input_filters = input_dict["analysis"]
			analyzer = text_analyzer.TextAnalyzer(input_string, input_filters)
			self.wfile.write((json.dumps(analyzer.analytics, indent=4, ensure_ascii=False) + "\n").encode())
			# self.send_response(200, "OK")
		except:
			# If control reaches here, it means the input is not in this format: {"text": "Necessary.", "analysis": "Optional."}
			error = "Incorrect input format!\n"
			self.wfile.write(bytes(error, 'utf-8'))
			# self.send_response(400, "Bad Request")


# Initializing the server
server = HTTPServer(('localhost', 8080), RequestHandler)
server.serve_forever()
