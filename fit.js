const table = document.getElementById("fit-table");
const thead = table.querySelector("thead");
const tbody = table.querySelector("tbody");

/**
 * Send an async AJAX request.
 * 
 * @param {String} method HTTP method. e.g., GET, POST, PUT, or DELETE
 * @param {String} url Where to send the request
 * @param {URLSearchParams} query
 * 	(optional) A URLSearchParams object, or
 * 	a String containing a URL query string (without the '?' prefix)
 * @param {Map} headers
 * 	(optional) A Map of potential additional headers.
 * @param {String} body (optional) request body
 * 
 * @returns Promise to completed XMLHttpRequest object
 */
const ajax = async function({method, url, query, headers, body, username, password}) {
	if (!method)
		throw new Error("No HTTP method");
	if (typeof url === "undefined")
		throw new Error("No URL");
	
	return new Promise((resolve, reject) => {
		const req = new XMLHttpRequest();
		req.onreadystatechange = () => {
			if (req.readyState == 4) {
				if (Math.floor(req.status / 100) == 2)
					resolve(req);
				else
					reject(req);
			}
		};
		if (query)
			url += "?" + query;
		req.open(method, url, true, username, password);
		if (headers)
			for (const [name, value] of headers)
				req.setRequestHeader(name, value)
		req.send(body);
	});
};

const updateInventory = function() {
	ajax({
		method: "GET",
		url: "inventory"
	}).then((req) => {
		console.log("responseText", req.responseText);
		data = JSON.parse(req.responseText);
		console.log("inventory:", data);
		if (!data.length)
			throw new Error("Inventory data error: " + data);
		{	const tr = document.createElement("tr");
			for (const cell of data[0]) {
				const th = document.createElement("th");
				th.innerText = cell;
				tr.append(th);
			}
			thead.append(tr);
		}
		for (let i = 1; i < data.length; i++) {
			const tr = document.createElement("tr");
			for (const cell of data[i]) {
				const td = document.createElement("td");
				td.innerText = cell;
				tr.append(td);
			}
			tbody.append(tr);
		}
	});
};

updateInventory();
