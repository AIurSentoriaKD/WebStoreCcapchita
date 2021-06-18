/* Utility functions*/
const _ = (id) => {
	return document.getElementById(id);
};
const formToJSON = (elements) =>
	[].reduce.call(
		elements,
		(data, element) => {
			data[element.name] = element.value;
			return data;
		},
		{}
	);

/* Handler Functions*/
function checkData(event) {
	event.preventDefault();
}

function submitData(event) {
	event.preventDefault();
}

function registerForm(event) {
	event.preventDefault();
	var form = _("register-form");
	var data = formToJSON(form.elements);
}

function countryList(event) {
	var el = event.target;
	_("country-error").innerText = "";
	if (el.value.length < 1) {
		_("country-datalist").innerHTML = "";
		return false;
	}
	var cicon = _("country-icon");
	cicon.classList.remove("fa-globe");
	cicon.classList.add("fa-spinner", "fa-fw");
	console.log(el.value);
	var request = new Request(
		window.location.protocol + "//www.pattaya-golfer.com/api.php",
		{
			method: "PUT",
			mode: "cors",
			headers: new Headers({
				"Content-Type": "application/json"
			}),
			body: JSON.stringify({
				action: "countrylist",
				query: el.value
			})
		}
	);

	fetch(request)
		.then(function (response) {
			return response.json();
		})
		.then(function (jsonobj) {
			if (jsonobj.success === true) {
				var cdl = _("country-datalist");
				cdl.options = {};

				var countries = jsonobj.countries;
				//			var countries = JSON.parse(jsonobj.countries);
				//			_('country-datalist').options = jsonobj.countries;
				/**/
				while (cdl.firstChild) {
					cdl.removeChild(cdl.firstChild);
				}
				countries.forEach(function (country) {
					console.log(country.name, "Country");

					var op = document.createElement("option");
					op.id = "country-" + country.code;
					op.value = country.name;
					//				op.text = country.name;
					cdl.appendChild(op);
				});
				/**/
			} else {
				_("country-error").innerText = jsonobj.message;
			}
		})
		.catch(function (error) {
			_("country-error").innerText = "Catch: " + error;
		});
	cicon.classList.remove("fa-spinner", "fa-fw");
	cicon.classList.add("fa-globe");
}
/* Document Ready Handler */
document.addEventListener("DOMContentLoaded", function () {
	var countrylist = _("country-list");
	countrylist.addEventListener("input", countryList);
	countrylist.addEventListener("click", function (event) {
		event.preventDefault();
	});
	/**
	countrylist.addEventListener('focus',function(event){
		event.target.value = '';
	});
	**/
	_("check-data").addEventListener("click", checkData);
	_("submit-data").addEventListener("click", submitData);
	_("register-form").addEventListener("submit", registerForm);
});