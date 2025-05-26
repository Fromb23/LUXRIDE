console.log("generate report loading")
document.addEventListener('DOMContentLoaded', function() {
    const dateRangeSelect = document.getElementById('date-range');
    const customDateRange = document.getElementById('custom-date-range');

    if (dateRangeSelect && customDateRange) {
        dateRangeSelect.addEventListener('change', function() {
            if (this.value === 'custom') {
                customDateRange.classList.remove('hidden');
            } else {
                customDateRange.classList.add('hidden');
            }
        });
    }

    const exportPdfBtn = document.getElementById('export-pdf');
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', function() {
            alert('PDF export functionality will be implemented here');
        });
    }

    const exportExcelBtn = document.getElementById('export-excel');
    if (exportExcelBtn) {
        exportExcelBtn.addEventListener('click', function() {
            alert('Excel export functionality will be implemented here');
        });
    }

   document.body.addEventListener('click', function(e) {
  const printBtn = e.target.closest('button');
  if (!printBtn || !printBtn.querySelector('.fa-print')) return;

  const userRow = printBtn.closest('tr');
  if (!userRow) return;

  // Extract data from the row
  const userName = userRow.querySelector('.text-gray-900').textContent;
  const userEmail = userRow.querySelector('.text-gray-500').textContent;
  const carDetails = userRow.querySelectorAll('td')[1].textContent.trim();
  const rentalPeriod = userRow.querySelectorAll('td')[2].textContent.trim();
  const status = userRow.querySelectorAll('td')[3].textContent.trim();
  const amount = userRow.querySelectorAll('td')[4].textContent.trim();

  // Create a nicely formatted print document
  const printWindow = window.open('', '', 'width=900,height=700');
  printWindow.document.write(`
    <html>
      <head>
        <title>Rental Receipt - ${userName}</title>
        <style>
          body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
          .receipt-container { max-width: 600px; margin: 20px auto; padding: 20px; }
          .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 20px; }
          .logo { font-size: 24px; font-weight: bold; color: #3cab4b; margin-bottom: 10px; }
          .title { font-size: 20px; margin-bottom: 5px; }
          .subtitle { color: #666; font-size: 14px; }
          .user-info { margin-bottom: 30px; }
          .info-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
          .info-table th { text-align: left; padding: 8px 0; width: 30%; color: #666; }
          .info-table td { padding: 8px 0; border-bottom: 1px solid #eee; }
          .amount { font-size: 18px; font-weight: bold; text-align: right; margin-top: 20px; }
          .footer { margin-top: 40px; text-align: center; font-size: 12px; color: #999; }
          .status {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
          }
          .status-completed { background: #e6ffed; color: #1a7f37; }
          .status-active { background: #e6f3ff; color: #1a56db; }
          .status-overdue { background: #ffebeb; color: #dc2626; }
          .status-pending { background: #fff8e6; color: #d97706; }
        </style>
      </head>
      <body>
        <div class="receipt-container">
          <div class="header">
            <div class="logo">LUXRIDE</div>
            <div class="title">Rental Receipt</div>
            <div class="subtitle">Generated on ${new Date().toLocaleDateString()}</div>
          </div>
          
          <div class="user-info">
            <h3>Customer Information</h3>
            <table class="info-table">
              <tr>
                <th>Name:</th>
                <td>${userName}</td>
              </tr>
              <tr>
                <th>Email:</th>
                <td>${userEmail}</td>
              </tr>
            </table>
          </div>
          
          <div class="rental-info">
            <h3>Rental Details</h3>
            <table class="info-table">
              <tr>
                <th>Vehicle:</th>
                <td>${carDetails}</td>
              </tr>
              <tr>
                <th>Rental Period:</th>
                <td>${rentalPeriod}</td>
              </tr>
              <tr>
                <th>Status:</th>
                <td><span class="status status-${status.toLowerCase()}">${status}</span></td>
              </tr>
            </table>
          </div>
          
          <div class="amount">
            Total Amount: ${amount}
          </div>
          
          <div class="footer">
            Thank you for choosing LuxRide<br>
            For any questions, please contact support@luxride.com
          </div>
        </div>
      </body>
    </html>
  `);
  
  printWindow.document.close();
  printWindow.focus();
  
  // Small delay to ensure content is loaded before printing
  setTimeout(() => {
    printWindow.print();
    printWindow.close();
  }, 200);
});

    

    document.querySelectorAll('button.text-yellow-500').forEach(button => {
        button.addEventListener('click', function() {
            alert('View details functionality will be implemented here');
        });
    });
});
