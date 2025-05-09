package com.payroll;
import com.itextpdf.text.*;
import com.itextpdf.text.pdf.PdfWriter;
import java.io.FileOutputStream;

public class EmployeeSalarySlip {

    public static void main(String[] args) {
        if (args.length < 6) {
            System.out.println("Please provide all arguments: employeeId, name, department, designation, salary, hometown");
            return;
        }

        // Debugging output
        System.out.println("Java program started");
        System.out.println("Arguments count: " + args.length);
        for (int i = 0; i < args.length; i++) {
            System.out.println("Arg " + i + ": " + args[i]);
        }

        // Get employee details
        int employeeId = Integer.parseInt(args[0]);
        String name = args[1];
        String department = args[2];
        String designation = args[3];
        double salary = Double.parseDouble(args[4]);
        String hometown = args[5];

        // Calculate tax and net salary
        double tax = calculateTax(salary);
        double netSalary = salary - tax;

        // Generate the PDF
        generatePDF(employeeId, name, department, designation, salary, hometown, tax, netSalary);

        // Debugging output for PDF generation
        System.out.println("Generated PDF for Employee ID: " + employeeId);
        System.out.println("Tax: " + tax);
        System.out.println("Net Salary: " + netSalary);
    }

    private static double calculateTax(double salary) {
        // Simple tax calculation
        return salary <= 50000 ? salary * 0.1 : salary * 0.2;
    }

    private static void generatePDF(int employeeId, String name, String department, String designation,
                                    double salary, String hometown, double tax, double netSalary) {
        Document document = new Document();
        try {
            // Ensure the 'static' folder exists
            new java.io.File("static").mkdirs();  // Create directory if it doesn't exist
            String filePath = "static/employee_" + employeeId + "_salary_slip.pdf";
            System.out.println("Saving PDF to: " + filePath);  // Debugging output

            PdfWriter.getInstance(document, new FileOutputStream(filePath));
            document.open();

            // Set fonts
            Font headerFont = new Font(Font.FontFamily.HELVETICA, 16, Font.BOLD);
            Font contentFont = new Font(Font.FontFamily.HELVETICA, 12, Font.NORMAL);

            // Add content to the document
            document.add(new Paragraph("Employee Salary Slip\n\n", headerFont));
            document.add(new Paragraph("Employee ID: " + employeeId, contentFont));
            document.add(new Paragraph("Name: " + name, contentFont));
            document.add(new Paragraph("Department: " + department, contentFont));
            document.add(new Paragraph("Designation: " + designation, contentFont));
            document.add(new Paragraph("Salary: " + salary, contentFont));
            document.add(new Paragraph("Hometown: " + hometown, contentFont));
            document.add(new Paragraph("Tax: " + tax, contentFont));
            document.add(new Paragraph("Net Salary: " + netSalary, contentFont));

            // Close the document
            document.close();
            System.out.println("PDF generated successfully at: " + filePath);  // Debugging output
        } catch (Exception e) {
            System.err.println("Error generating PDF: " + e.getMessage());
            e.printStackTrace();  // This will give more details if something goes wrong
        }
    }
}
