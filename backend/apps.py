from django.apps import AppConfig


class BackendConfig(AppConfig):
    name = 'backend'

class filterOptions():
	filter_options = ["Company_Name", "System_Name", 
					  "Serial_Number", "Product_Family"]

	def get_filters():
		return filter_options

	def add_filter(new_filt):
		filter_options.append(new_filt)
