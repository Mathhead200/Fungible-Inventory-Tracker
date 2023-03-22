from flask import *
from openpyxl import *

wb = load_workbook(filename = "fit.xlsx")
inventory = wb["Inventory"]
rooms = wb["Rooms"]
assets = wb["Assets"]
log = wb["Log"]

def collect_sheet(sheet):
	header = next(sheet.rows)
	body = sheet.iter_rows(min_row=2, max_col=len(header))
	return {row[0].value: {key.value: cell.value for (key, cell) in zip(header, row)} for row in body}

def sort_sheet(sheet):
	D = collect_sheet(sheet)
	return [D[k] for k in sorted(D.keys())]

app = Flask(__name__)

@app.route("/")
def flask_root():
	return ""

@app.route("/asset", methods=["GET"])
def get_assets():
	return collect_sheet(assets)

@app.route("/asset", methods=["POST"])
def create_asset():
	pass

@app.route("/asset/<int:id>", methods=["GET"])
def asset_info(id):
	pass

@app.route("/asset/<int:id>", methods=["PUT"])
def update_asset_info(id):
	pass

@app.route("/asset/<int:id>", methods=["DELETE"])
def remove_asset(id):
	pass

@app.route("/room", methods=["GET"])
def get_rooms():
	return collect_sheet(rooms)

@app.route("/room", methods=["POST"])
def create_room():
	pass

@app.route("/room/<int:id>", methods=["GET"])
def room_info():
	pass

@app.route("/room/<int:id>", methods=["PUT"])
def update_room_info():
	pass

@app.route("/room/<int:id>", methods=["DELETE"])
def delete_room():
	pass

@app.route("/move", methods=["POST"])
def move_asset():
	pass

@app.route("/split", methods=["POST"])
def split_asset():
	pass

@app.route("/merge", methods=["POST"])
def merge_assets():
	pass

@app.route("/inventory", methods=["GET"])
def inventory_table():
	def h(L, pk):
		return {L[i][pk]: i for i in range(len(L))}
	as_list = sort_sheet(assets)
	rm_list = sort_sheet(rooms)
	as_hash = h(as_list, "Asset ID")
	rm_hash = h(rm_list, "Room ID")

	table = [["Room"] + [a["Asset Name"] for a in as_list]]
	table.extend([[[r["Room Name"]] + [0] * len(as_list)] for r in rm_list])
	
	header = [cell.value for cell in next(inventory.rows)]
	ROOM_ID = header.index("Room ID")
	ASSET_ID = header.index("Asset ID")
	QUANTITY = header.index("Quantity")

	for row in inventory.iter_rows(min_row=2):
		rm_idx = rm_hash[row[ROOM_ID]]
		as_idx = as_hash[row[ASSET_ID]]
		table[rm_idx][as_idx] += int(row[QUANTITY])
	
	return table
