import './pos/pos.js';
import './reports/reports.js';
import './inventory/inventory.js';

// Initialize app
frappe.provide('wasper_inventory');

wasper_inventory.init = function() {
    // Initialize modules
    wasper_inventory.pos.init();
    wasper_inventory.reports.init();
    wasper_inventory.inventory.init();
};

// Run when DOM is ready
$(document).ready(function() {
    wasper_inventory.init();
}); 