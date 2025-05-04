<?php
// Set headers for JSON response
header('Content-Type: application/json');

// Allow cross-origin requests (if needed)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get JSON input from POST request
$json_data = file_get_contents('php://input');
$data = json_decode($json_data, true);

// Debug: Log the received data
error_log("Received data: " . print_r($data, true));

// Check if data was properly decoded
if ($data === null) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid JSON data']);
    exit;
}

// Validate required fields
if (empty($data['name']) || empty($data['disease_name']) || empty($data['birth_date']) || empty($data['admission_date'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Missing required fields']);
    exit;
}

// Connect to Oracle database using OCI8
try {
    // Oracle connection details
    // $username = 'system';
    // $password = 'Abdo2004@';
    // $connection_string = 'localhost:1521/FREE';
    $username = 'system';
    $password = 's2004b22';
    $connection_string = '192.168.21.1:1521/FREE';
    
    // Create connection
    $conn = oci_connect($username, $password, $connection_string);
    
    if (!$conn) {
        $e = oci_error();
        throw new Exception('Database connection error: ' . $e['message']);
    }
    
    // Begin transaction - we'll use OCI_DEFAULT for all executions to allow rollback
    
    // Format dates for Oracle
    $birth_date = date('d-M-Y', strtotime($data['birth_date']));
    $admission_date = date('d-M-Y', strtotime($data['admission_date']));
    
    // Insert into PATIENT table
    $patient_query = "INSERT INTO patient (name, birth_date, admission_date, status, notes) 
                     VALUES (:name, TO_DATE(:birth_date, 'DD-MON-YYYY'), 
                            TO_DATE(:admission_date, 'DD-MON-YYYY'), :status, :notes)
                     RETURNING patient_id INTO :patient_id";
    
    $patient_stmt = oci_parse($conn, $patient_query);
    
    if (!$patient_stmt) {
        $e = oci_error($conn);
        throw new Exception('Failed to prepare patient statement: ' . $e['message']);
    }
    
    // Set default status if empty
    $status = !empty($data['status']) ? $data['status'] : 'STABLE';
    $notes = !empty($data['notes']) ? $data['notes'] : '';
    
    // Bind parameters
    oci_bind_by_name($patient_stmt, ':name', $data['name']);
    oci_bind_by_name($patient_stmt, ':birth_date', $birth_date);
    oci_bind_by_name($patient_stmt, ':admission_date', $admission_date);
    oci_bind_by_name($patient_stmt, ':status', $status);
    oci_bind_by_name($patient_stmt, ':notes', $notes);
    
    // Bind the output parameter
    $patient_id = 0;
    oci_bind_by_name($patient_stmt, ':patient_id', $patient_id, -1, SQLT_INT);
    
    // Execute the patient insert
    $result = oci_execute($patient_stmt, OCI_DEFAULT);
    
    if (!$result) {
        $e = oci_error($patient_stmt);
        throw new Exception('Failed to insert patient: ' . $e['message']);
    }
    
    // Close patient statement
    oci_free_statement($patient_stmt);
    
    // Insert into DISEASE table
    $disease_query = "INSERT INTO disease (patient_id, disease_name) VALUES (:patient_id, :disease_name)";
    $disease_stmt = oci_parse($conn, $disease_query);
    
    if (!$disease_stmt) {
        $e = oci_error($conn);
        throw new Exception('Failed to prepare disease statement: ' . $e['message']);
    }
    
    // Bind parameters
    oci_bind_by_name($disease_stmt, ':patient_id', $patient_id);
    oci_bind_by_name($disease_stmt, ':disease_name', $data['disease_name']);
    
    // Execute disease insert
    $result = oci_execute($disease_stmt, OCI_DEFAULT);
    
    if (!$result) {
        $e = oci_error($disease_stmt);
        throw new Exception('Failed to insert disease: ' . $e['message']);
    }
    
    // Close disease statement
    oci_free_statement($disease_stmt);
    
    // Insert symptoms if any
    if (!empty($data['symptoms']) && is_array($data['symptoms'])) {
        $symptom_query = "INSERT INTO symptoms (patient_id, symptom_name, severity) 
                         VALUES (:patient_id, :symptom_name, :severity)";
        
        foreach ($data['symptoms'] as $symptom_data) {
            // Each symptom should be an array with name and severity
            $symptom_name = is_array($symptom_data) ? $symptom_data[0] : $symptom_data;
            $severity = is_array($symptom_data) ? $symptom_data[1] : 'Mild';
            
            $symptom_stmt = oci_parse($conn, $symptom_query);
            
            if (!$symptom_stmt) {
                $e = oci_error($conn);
                throw new Exception('Failed to prepare symptom statement: ' . $e['message']);
            }
            
            // Bind parameters
            oci_bind_by_name($symptom_stmt, ':patient_id', $patient_id);
            oci_bind_by_name($symptom_stmt, ':symptom_name', $symptom_name);
            oci_bind_by_name($symptom_stmt, ':severity', $severity);
            
            // Execute symptom insert
            $result = oci_execute($symptom_stmt, OCI_DEFAULT);
            
            if (!$result) {
                $e = oci_error($symptom_stmt);
                throw new Exception('Failed to insert symptom: ' . $e['message']);
            }
            
            // Free symptom statement
            oci_free_statement($symptom_stmt);
        }
    }
    
    // Commit transaction
    $commit = oci_commit($conn);
    
    if (!$commit) {
        $e = oci_error($conn);
        throw new Exception('Failed to commit transaction: ' . $e['message']);
    }
    
    // Close connection
    oci_close($conn);
    
    // Return success response
    http_response_code(200);
    echo json_encode([
        'success' => true, 
        'message' => 'Patient added successfully',
        'patient_id' => $patient_id
    ]);
    
} catch (Exception $e) {
    // If connection exists, rollback transaction
    if (isset($conn) && $conn) {
        oci_rollback($conn);
        oci_close($conn);
    }
    
    // Return error response with detailed information
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => $e->getMessage()
    ]);
    
    // Log the error
    error_log("Patient API error: " . $e->getMessage());
}
?>