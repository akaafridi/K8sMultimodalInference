import os
import logging
from flask import Flask, request, jsonify, render_template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Homepage with information about the API"""
    # Return HTML template for a more user-friendly interface
    return render_template('index.html', 
                          version="1.0.0", 
                          status="running")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness and readiness probes"""
    return jsonify({"status": "healthy"}), 200

@app.route('/infer', methods=['POST'])
def infer():
    """
    Model inference endpoint. Accepts JSON input for inference requests.
    
    Example payload:
    {
        "data": "your input data here"
    }
    
    Returns:
    {
        "predictions": "model prediction result",
        "model_version": "version of the model used"
    }
    """
    try:
        # Get JSON data from request
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({"error": "No input data provided"}), 400
        
        input_data = request_data.get('data')
        if not input_data:
            return jsonify({"error": "Missing 'data' field in request"}), 400
        
        # Log the inference request
        logger.info(f"Received inference request: {input_data[:100]}...")
        
        # TODO: Add your actual model inference code here
        # This is where you would load your model and perform inference
        # For demonstration purposes, we're just returning a placeholder
        
        # Placeholder inference result
        result = {
            "predictions": f"Processed: {input_data[:100]}...",
            "model_version": "1.0.0"
        }
        
        logger.info("Inference completed successfully")
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Log server startup
    logger.info(f"Starting model server on port {port}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
