frappe.provide("wasper_inventory.pos");

wasper_inventory.pos.POS = class POS {
    constructor(frm) {
        this.frm = frm;
        this.setup();
    }

    setup() {
        this.setup_items();
        this.setup_payments();
        this.setup_events();
    }

    setup_items() {
        this.frm.set_query("item_code", "items", () => {
            return {
                filters: {
                    "disabled": 0
                }
            };
        });
    }

    setup_payments() {
        this.frm.set_query("mode_of_payment", "payments", () => {
            return {
                filters: {
                    "enabled": 1
                }
            };
        });
    }

    setup_events() {
        this.frm.fields_dict.items.grid.get_field("item_code").get_query = () => {
            return {
                filters: {
                    "disabled": 0
                }
            };
        };

        this.frm.fields_dict.items.grid.get_field("qty").onchange = () => {
            this.calculate_totals();
        };

        this.frm.fields_dict.items.grid.get_field("rate").onchange = () => {
            this.calculate_totals();
        };
    }

    calculate_totals() {
        let total = 0;
        let total_qty = 0;

        this.frm.doc.items.forEach(item => {
            total += flt(item.qty) * flt(item.rate);
            total_qty += flt(item.qty);
        });

        this.frm.set_value("total_qty", total_qty);
        this.frm.set_value("total", total);
        this.frm.set_value("grand_total", total);
    }
}; 