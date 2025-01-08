# Copyright (c) 2025, Kalutu and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Shop(WebsiteGenerator):
    def on_load(self):
        update_shop_count(self)

    def on_update(self):
        update_shop_count(self)

    def on_trash(self):
        update_shop_count(self)


def update_shop_count(shop):
    if not shop.airport:
        return

    airport = frappe.get_doc("Airport", shop.airport)
    total_shop_count = frappe.db.count("Shop", filters={"airport": shop.airport})
    occupied_shop_count = frappe.db.count("Shop", filters={"airport": shop.airport, "status":"Occupied"})
    vacant_shop_count = frappe.db.count("Shop", filters={"airport": shop.airport, "status":"Vacant"})

    airport.db_set("total_shops", total_shop_count)
    airport.db_set("shops_occupied", occupied_shop_count)
    airport.db_set("shops_available", vacant_shop_count)
