"""UBL XML İş Kuralı Motoru.

Problem: XML okunabilir olsa bile faturanın miktar, para birimi ve toplamlarının çelişmesini saptamak.
Method: Namespace, Decimal, tutar ve vergi tutarlılığı
Invariant: Basitleştirilmiş pozitif fatura profili, satır iskonto/masrafı ve tek para birimi kullanılır.
Boundary: GİB uygunluk sertifikası veya tam XSD/Schematron doğrulaması değildir; tevkifat, döviz ve özel vergi profilleri ayrıca gerekir."""
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET
from datetime import date
NS = {'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2', 'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'}
INVOICE = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'

def validate(xml, max_bytes=200000):
    data = xml.encode('utf-8')
    findings = []

    def add(rule, path, message):
        findings.append({'rule': rule, 'path': path, 'severity': 'ERROR', 'message': message})
    if len(data) > max_bytes:
        return [{'rule': 'SIZE', 'path': '/', 'severity': 'ERROR', 'message': 'document too large'}]
    if '<!DOCTYPE' in xml.upper() or '<!ENTITY' in xml.upper():
        return [{'rule': 'DTD', 'path': '/', 'severity': 'ERROR', 'message': 'DTD/entity declarations are not supported'}]
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        return [{'rule': 'XML_PARSE', 'path': '/', 'severity': 'ERROR', 'message': str(exc)}]
    if root.tag != '{' + INVOICE + '}Invoice':
        add('ROOT_NAMESPACE', '/', 'expected UBL Invoice namespace')
    for path in ['cbc:ID', 'cbc:IssueDate', 'cbc:DocumentCurrencyCode']:
        if not root.findtext(path, default='', namespaces=NS).strip():
            add('REQUIRED', path, 'missing value')
    try:
        date.fromisoformat(root.findtext('cbc:IssueDate', default='', namespaces=NS))
    except ValueError:
        add('DATE', 'cbc:IssueDate', 'expected valid ISO date')
    currency = root.findtext('cbc:DocumentCurrencyCode', namespaces=NS)
    total = Decimal(0)
    tax = Decimal(0)
    ids = set()

    def number(parent, path, label):
        node = parent.find(path, NS)
        if node is None:
            add('AMOUNT_REQUIRED', label, 'missing numeric field')
            return None
        try:
            n = Decimal(node.text or '')
            if not n.is_finite():
                raise InvalidOperation
        except InvalidOperation:
            add('DECIMAL', label, 'invalid finite decimal')
            return None
        if node.get('currencyID') and node.get('currencyID') != currency:
            add('CURRENCY', label, 'amount currency differs')
        return n
    lines = root.findall('cac:InvoiceLine', NS)
    if not lines:
        add('LINES_REQUIRED', 'cac:InvoiceLine', 'at least one line required')
    for index, line in enumerate(lines, 1):
        path = f'InvoiceLine[{index}]'
        identifier = line.findtext('cbc:ID', namespaces=NS)
        if not identifier or identifier in ids:
            add('LINE_ID', path, 'line ID missing or duplicated')
        ids.add(identifier)
        qty = number(line, 'cbc:InvoicedQuantity', path + '/quantity')
        price = number(line, 'cac:Price/cbc:PriceAmount', path + '/price')
        amount = number(line, 'cbc:LineExtensionAmount', path + '/amount')
        if qty is not None and qty <= 0:
            add('QUANTITY', path, 'quantity must be positive for this invoice profile')
        allowance = Decimal(0)
        for ac in line.findall('cac:AllowanceCharge', NS):
            value = number(ac, 'cbc:Amount', path + '/adjustment')
            if value is not None:
                allowance += value if ac.findtext('cbc:ChargeIndicator', namespaces=NS) == 'true' else -value
        if qty is not None and price is not None and (amount is not None) and (abs(qty * price + allowance - amount) > Decimal('.01')):
            add('LINE_ARITHMETIC', path, 'quantity × price plus adjustments differs')
        if amount is not None:
            total += amount
        value = number(line, 'cac:TaxTotal/cbc:TaxAmount', path + '/tax')
        if value is not None:
            tax += value
    root_tax = root.find('cac:TaxTotal', NS)
    if root_tax is not None:
        declared_tax = number(root_tax, 'cbc:TaxAmount', 'total/tax')
        if declared_tax is not None and abs(declared_tax - tax) > Decimal('.01'):
            add('TAX_SUM', 'total/tax', 'root tax differs from line tax sum')
    legal = root.find('cac:LegalMonetaryTotal', NS)
    if legal is None:
        add('TOTAL_REQUIRED', 'LegalMonetaryTotal', 'missing totals')
    else:
        net = number(legal, 'cbc:LineExtensionAmount', 'total/net')
        payable = number(legal, 'cbc:PayableAmount', 'total/payable')
        if net is not None and abs(net - total) > Decimal('.01'):
            add('LINE_SUM', 'total/net', 'line sum mismatch')
        if payable is not None and abs(payable - total - tax) > Decimal('.01'):
            add('PAYABLE', 'total/payable', 'simplified net + tax mismatch')
    return findings

def run(config):
    return {'documents': [{'id': d['id'], 'findings': validate(d['xml']), 'valid_in_supported_rules': not validate(d['xml'])} for d in config['documents']], 'scope': 'XML parsing and a limited business-rule profile; not GIB XSD/Schematron certification'}

import argparse, json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Run reproducible synthetic project scenario')
    parser.add_argument('command', choices=['demo'])
    parser.add_argument('--input', default='scenario.json')
    parser.add_argument('--output', default='report.json')
    args = parser.parse_args()
    report = run(json.loads(Path(args.input).read_text(encoding='utf-8')))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    print(f'Report: {target}')
if __name__ == '__main__':
    main()
