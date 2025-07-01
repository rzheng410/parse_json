import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class BillingSchemaParser:
    def __init__(self, schemas_dir: str = "schemas_output"):
        self.schemas_dir = schemas_dir
        self.target_schemas = {
            "invoice_generated": "billing.lifecycle.invoice_generated.json",
            "payment_method_added": "billing.lifecycle.payment_method_added.json", 
            "awarded_credit": "billing.lifecycle.awarded_credit.json",
            "card_charged_failed": "billing.lifecycle.card_charged_failed.json",
            "failed_month_close_charge": "billing.lifecycle.failed_month_close_charge.json",
            "account_state_updated": "billing.lifecycle.account_state_updated.json"
        }
        
    def load_schema_file(self, filename: str) -> List[Dict[str, Any]]:
        """Load and parse a JSON schema file."""
        filepath = os.path.join(self.schemas_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File {filename} not found")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing {filename}: {e}")
            return []
    
    def extract_schema_info(self, schema_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract key information from schema data."""
        if not schema_data:
            return {}
        
        # Take the first schema definition (they appear to be duplicates)
        schema = schema_data[0]
        
        # Extract the main schema definition
        schema_ref = schema.get("$ref", "")
        defs = schema.get("$defs", {})
        
        # Find the main schema object
        main_schema_name = schema_ref.split("/")[-1] if schema_ref else None
        main_schema = defs.get(main_schema_name, {}) if main_schema_name else {}
        
        return {
            "schema_name": main_schema_name,
            "properties": main_schema.get("properties", {}),
            "required_fields": main_schema.get("required", []),
            "type": main_schema.get("type", "object"),
            "additional_properties": main_schema.get("additionalProperties", True)
        }
    
    def parse_invoice_generated(self) -> Dict[str, Any]:
        """Parse invoice generated schema."""
        data = self.load_schema_file(self.target_schemas["invoice_generated"])
        schema_info = self.extract_schema_info(data)
        
        return {
            "event_type": "Invoice Generated",
            "description": "Schema for invoice generation events",
            "fields": {
                "event_time": {"type": "string", "format": "date-time", "required": True},
                "resource_urn": {"type": "string", "required": True},
                "invoice_total": {"type": "string", "required": True},
                "invoice_segment": {"type": "string", "required": True}
            }
        }
    
    def parse_payment_method_added(self) -> Dict[str, Any]:
        """Parse payment method added schema."""
        data = self.load_schema_file(self.target_schemas["payment_method_added"])
        schema_info = self.extract_schema_info(data)
        
        return {
            "event_type": "Payment Method Added",
            "description": "Schema for payment method addition events",
            "fields": {
                "actor_urn": {"type": "string", "required": True},
                "event_time": {"type": "string", "format": "date-time", "required": True},
                "resource_urn": {"type": "string", "required": True},
                "success": {"type": "boolean", "required": True},
                "payment_method": {
                    "type": "object",
                    "required": True,
                    "nested_fields": {
                        "payment_method_id": {"type": "integer", "required": True},
                        "payment_method_type": {"type": "string", "required": True},
                        "external_payment_method_id": {"type": "string", "required": True},
                        "fingerprint": {"type": "string", "required": True}
                    }
                }
            }
        }
    
    def parse_awarded_credit(self) -> Dict[str, Any]:
        """Parse awarded credit schema."""
        data = self.load_schema_file(self.target_schemas["awarded_credit"])
        schema_info = self.extract_schema_info(data)
        
        return {
            "event_type": "Awarded Credit",
            "description": "Schema for credit award events",
            "fields": {
                "event_time": {"type": "string", "format": "date-time", "required": True},
                "actor_urn": {"type": "string", "required": True},
                "resource_urn": {"type": "string", "required": True},
                "expiring_credit": {
                    "type": "object",
                    "required": True,
                    "nested_fields": {
                        "id": {"type": "integer", "required": True},
                        "description": {"type": "string", "required": True},
                        "issue_amount": {"type": "string", "required": True},
                        "remaining_amount": {"type": "string", "required": True},
                        "category": {"type": "string", "required": True},
                        "sub_category": {"type": "string", "required": True},
                        "issue_date": {"type": "string", "format": "date-time", "required": True},
                        "expiration_date": {"type": "string", "format": "date-time", "required": True}
                    }
                }
            }
        }
    
    def parse_card_charged_failed(self) -> Dict[str, Any]:
        """Parse card charge failed schema."""
        data = self.load_schema_file(self.target_schemas["card_charged_failed"])
        schema_info = self.extract_schema_info(data)
        
        return {
            "event_type": "Card Charge Failed",
            "description": "Schema for failed card charge events",
            "fields": {
                "actor_urn": {"type": "string", "required": True},
                "event_time": {"type": "string", "format": "date-time", "required": True},
                "resource_urn": {"type": "string", "required": True},
                "charge_transaction_id": {"type": "integer", "required": True},
                "decline_code": {"type": "string", "required": True}
            }
        }
    
    def parse_failed_month_close_charge(self) -> Dict[str, Any]:
        """Parse failed month close charge schema."""
        data = self.load_schema_file(self.target_schemas["failed_month_close_charge"])
        schema_info = self.extract_schema_info(data)
        
        return {
            "event_type": "Failed Month Close Charge",
            "description": "Schema for failed month-end charge events",
            "fields": {
                "event_time": {"type": "string", "format": "date-time", "required": True},
                "resource_urn": {"type": "string", "required": True},
                "amount": {"type": "string", "required": True},
                "invoice_id": {"type": "integer", "required": True}
            }
        }
    
    def parse_account_state_updated(self) -> Dict[str, Any]:
        """Parse account state updated schema."""
        data = self.load_schema_file(self.target_schemas["account_state_updated"])
        schema_info = self.extract_schema_info(data)
        
        return {
            "event_type": "Account State Updated",
            "description": "Schema for account state update events",
            "fields": {
                "event_time": {"type": "string", "format": "date-time", "required": True},
                "resource_urn": {"type": "string", "required": True},
                "actor_urn": {"type": "string", "required": False},  # Optional in some variants
                "state_name": {"type": "string", "required": True},
                "state_value": {"type": "string", "required": True},
                "state_note": {"type": "string", "required": True}
            }
        }
    
    def parse_all_schemas(self) -> Dict[str, Any]:
        """Parse all target schemas and return comprehensive results."""
        results = {
            "parsed_at": datetime.now().isoformat(),
            "total_schemas": len(self.target_schemas),
            "schemas": {}
        }
        
        # Parse each schema
        results["schemas"]["invoice_generated"] = self.parse_invoice_generated()
        results["schemas"]["payment_method_added"] = self.parse_payment_method_added()
        results["schemas"]["awarded_credit"] = self.parse_awarded_credit()
        results["schemas"]["card_charged_failed"] = self.parse_card_charged_failed()
        results["schemas"]["failed_month_close_charge"] = self.parse_failed_month_close_charge()
        results["schemas"]["account_state_updated"] = self.parse_account_state_updated()
        
        return results
    
    def generate_field_summary(self) -> Dict[str, Any]:
        """Generate a summary of all fields across schemas."""
        all_schemas = self.parse_all_schemas()
        
        field_summary = {
            "common_fields": {},
            "unique_fields": {},
            "field_types": {},
            "required_fields_by_schema": {}
        }
        
        # Collect all fields
        for schema_name, schema_data in all_schemas["schemas"].items():
            fields = schema_data.get("fields", {})
            field_summary["required_fields_by_schema"][schema_name] = []
            
            for field_name, field_info in fields.items():
                field_type = field_info.get("type", "unknown")
                
                # Track field types
                if field_type not in field_summary["field_types"]:
                    field_summary["field_types"][field_type] = []
                field_summary["field_types"][field_type].append(f"{schema_name}.{field_name}")
                
                # Track required fields
                if field_info.get("required", False):
                    field_summary["required_fields_by_schema"][schema_name].append(field_name)
                
                # Track unique fields
                if field_name not in field_summary["unique_fields"]:
                    field_summary["unique_fields"][field_name] = []
                field_summary["unique_fields"][field_name].append(schema_name)
        
        # Identify common fields (appearing in multiple schemas)
        for field_name, schemas in field_summary["unique_fields"].items():
            if len(schemas) > 1:
                field_summary["common_fields"][field_name] = schemas
        
        return field_summary
    
    def save_results(self, results: Dict[str, Any], output_file: str = "parsed_schemas.json"):
        """Save parsing results to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_file}")
    
    def print_summary(self):
        """Print a human-readable summary of the parsed schemas."""
        results = self.parse_all_schemas()
        field_summary = self.generate_field_summary()
        
        print("=" * 60)
        print("BILLING SCHEMA PARSING SUMMARY")
        print("=" * 60)
        print(f"Parsed {results['total_schemas']} schemas at {results['parsed_at']}")
        print()
        
        for schema_name, schema_data in results["schemas"].items():
            print(f"📋 {schema_data['event_type']}")
            print(f"   Description: {schema_data['description']}")
            print(f"   Fields: {len(schema_data['fields'])}")
            
            required_fields = [name for name, info in schema_data["fields"].items() 
                             if info.get("required", False)]
            print(f"   Required fields: {', '.join(required_fields)}")
            print()
        
        print("=" * 60)
        print("FIELD ANALYSIS")
        print("=" * 60)
        
        print(f"Common fields (appearing in multiple schemas):")
        for field, schemas in field_summary["common_fields"].items():
            print(f"  • {field}: {', '.join(schemas)}")
        
        print(f"\nField types found:")
        for field_type, fields in field_summary["field_types"].items():
            print(f"  • {field_type}: {len(fields)} fields")
        
        print("=" * 60)

def main():
    """Main function to run the schema parser."""
    parser = BillingSchemaParser()
    
    # Parse all schemas
    results = parser.parse_all_schemas()
    
    # Generate and print summary
    parser.print_summary()
    
    # Save results
    parser.save_results(results)
    
    # Also save field summary
    field_summary = parser.generate_field_summary()
    parser.save_results(field_summary, "field_summary.json")
    
    print("\n✅ Schema parsing completed successfully!")
    print("�� Check 'parsed_schemas.json' for detailed results")
    print("📁 Check 'field_summary.json' for field analysis")

if __name__ == "__main__":
    main()