# Wasper Inventory

A comprehensive inventory management solution built on Frappe Framework.

## Features

- Multi-branch inventory management
- Point of Sale (POS) system
- Stock management and tracking
- Automated email notifications
- Comprehensive reporting
- Branch performance analytics

## Installation

1. Install Frappe Framework:
```bash
bench init frappe-bench
cd frappe-bench
```

2. Create a new site:
```bash
bench new-site wasper.local
```

3. Install Wasper Inventory:
```bash
bench get-app wasper_inventory https://github.com/wasper/wasper_inventory
bench --site wasper.local install-app wasper_inventory
```

## Configuration

1. Set up branches:
   - Go to: Branch > New
   - Enter branch details
   - Assign branch manager

2. Configure POS:
   - Go to: POS Profile > New
   - Set up payment methods
   - Configure users

3. Set up email notifications:
   - Configure email server
   - Set up notification schedules

## Usage

### POS System

1. Access POS:
   - Go to: POS
   - Select branch and POS profile
   - Start selling

2. Process sales:
   - Add items to cart
   - Select payment method
   - Complete transaction

### Inventory Management

1. Stock management:
   - Track stock levels
   - Set reorder points
   - Manage warehouses

2. Stock transfers:
   - Create stock entries
   - Transfer between branches
   - Update stock levels

### Reports

1. Sales reports:
   - Branch-wise sales
   - Item-wise sales
   - POS summary

2. Stock reports:
   - Stock balance
   - Stock movement
   - Low stock alerts

## API Documentation

### POS API

```python
# Create POS Invoice
pos_invoice = frappe.new_doc("POS Invoice")
pos_invoice.customer = "CUST-001"
pos_invoice.branch = "BRANCH-001"
pos_invoice.append("items", {
    "item_code": "ITEM-001",
    "qty": 1,
    "rate": 100
})
pos_invoice.submit()
```

### Stock API

```python
# Create Stock Entry
stock_entry = frappe.new_doc("Stock Entry")
stock_entry.stock_entry_type = "Material Receipt"
stock_entry.branch = "BRANCH-001"
stock_entry.append("items", {
    "item_code": "ITEM-001",
    "qty": 10,
    "basic_rate": 100
})
stock_entry.submit()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For support, email support@wasper.com 