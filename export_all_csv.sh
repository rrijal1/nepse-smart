#!/bin/bash
# NEPSE Smart - Bulk CSV Export Script
# Exports all PostgreSQL tables to CSV files

echo "=== NEPSE Smart - Bulk CSV Export ==="
echo "Exporting all PostgreSQL tables to CSV format..."
echo ""

# Create exports directory
mkdir -p csv_exports

# Export each table with progress indicators
echo "📊 Exporting historical_price_volume (market data)..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.historical_price_volume ORDER BY business_date DESC, symbol) TO STDOUT WITH CSV HEADER;" > csv_exports/historical_price_volume.csv

echo "🏛️ Exporting floorsheet (trading transactions)..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.floorsheet ORDER BY date DESC, stock_symbol) TO STDOUT WITH CSV HEADER;" > csv_exports/floorsheet.csv

echo "📈 Exporting market_indices..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.market_indices ORDER BY date DESC, index_name) TO STDOUT WITH CSV HEADER;" > csv_exports/market_indices.csv

echo "💱 Exporting exchange_rates..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.exchange_rates ORDER BY date DESC, currency) TO STDOUT WITH CSV HEADER;" > csv_exports/exchange_rates.csv

echo "🏦 Exporting banking_indicators..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.banking_indicators ORDER BY date DESC, indicator) TO STDOUT WITH CSV HEADER;" > csv_exports/banking_indicators.csv

echo "📊 Exporting short_term_rates..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.short_term_rates ORDER BY date DESC, maturity) TO STDOUT WITH CSV HEADER;" > csv_exports/short_term_rates.csv

echo "📋 Exporting watchlist..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM watchlist ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/watchlist.csv

echo "💼 Exporting portfolio..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM portfolio ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/portfolio.csv

echo "💰 Exporting transactions..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM transactions ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/transactions.csv

echo "🎯 Exporting paper_accounts..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_accounts ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_accounts.csv

echo "📈 Exporting paper_portfolio..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_portfolio ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_portfolio.csv

echo "📊 Exporting paper_transactions..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_transactions ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_transactions.csv

echo "� Exporting table inventory (names only)..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT schemaname || '.' || tablename as full_table_name, schemaname, tablename FROM pg_tables WHERE schemaname IN ('public', 'nepse_data') ORDER BY schemaname, tablename) TO STDOUT WITH CSV HEADER;" > csv_exports/table_names_only.csv

echo "📊 Exporting detailed table inventory (with metadata)..."
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT schemaname, tablename, tableowner, hasindexes, hasrules, hastriggers, rowsecurity FROM pg_tables WHERE schemaname IN ('public', 'nepse_data') ORDER BY schemaname, tablename) TO STDOUT WITH CSV HEADER;" > csv_exports/all_tables_inventory.csv

echo ""
echo "=== Export Complete ==="
echo "Files exported to: csv_exports/"
ls -lah csv_exports/

echo ""
echo "=== Record Counts ==="
for file in csv_exports/*.csv; do
    if [[ "$file" == *"inventory"* ]] || [[ "$file" == *"names"* ]]; then
        count=$(($(wc -l < "$file") - 1))
        echo "$(basename "$file" .csv): $count tables listed"
    else
        count=$(($(wc -l < "$file") - 1))
        echo "$(basename "$file" .csv): $count records"
    fi
done

echo ""
echo "✅ All PostgreSQL tables exported to CSV successfully!"
echo "📁 Files are ready for analysis in Excel, Google Sheets, or any data tool."