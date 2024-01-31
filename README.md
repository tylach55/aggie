# aggie

setup your virtual environment on macOS
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install flask


A prototype for an agriculture crm/erp

Running The App On Command Line In this directory
	-Create a python virtual environment 
		-python3 -m venv .venv
	-Activate virtual environment
		. .venv/bin/activates
	-intall flask
		pip3 install Flask


-----User Stories------
With the CRM app
	-* as a user I could order produce
		-as a user I want to be able to pay for my order
		-as a user ordering produce I could see when my order arrives
		-as a user ordering produce I could see how much my order costs
		-as a user ordering produce I could track my order
	-* as a user I could browse produce options (Wheat Walnuts Almonds)
	-* as a user I could find ways to contact the Buisness owner
	-* as an owner I could "hype up" my buisness
	- as an owner I want to remember customers
	- as eveyone except a hacker I want a safe and secure website
		-as a user I want the app to forget my payment information

		!!!!!! Make More Security Consideratoins Later !!!!!!!!! 

With the ERP
	-* as a seller I want to keep inventory of my available produce
	-* as a harvester I want an easy way to add a harvest to inventory
	-* as a shipper I want an easy way to remove a shipment from inventory
	-* as a shipper I want to keep track of outstanding shipments 
	-* as an accountant I want to keep track of payroll
	-* as a salesman I want to be able to keep track of personal potential leads

