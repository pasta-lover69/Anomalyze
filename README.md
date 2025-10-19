# Anomalyze 🔍

**High-Performance Network Intrusion Detection System using Machine Learning**

Anomalyze is an optimized network anomaly detection system that uses ensemble K-means clustering to identify suspicious network traffic patterns and potential cyber threats with exceptional speed and accuracy.

> 📚 **For developers and contributors:** See [DEVELOPMENT_DOCS.md](DEVELOPMENT_DOCS.md) for detailed technical documentation, model training, optimization details, and troubleshooting.

![Python](https://img.shields.io/badge/python-v3.14+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-v1.4+-orange.svg)
![Chart.js](https://img.shields.io/badge/Chart.js-v4.0+-ff6384.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Performance](https://img.shields.io/badge/speed-47K%20samples%2Fsec-brightgreen.svg)
![Accuracy](https://img.shields.io/badge/accuracy-77.75%25-brightgreen.svg)
![Silhouette](https://img.shields.io/badge/cluster%20quality-97.51%25-brightgreen.svg)
![F1](https://img.shields.io/badge/F1--score-79.19%25-green.svg)

## 🚀 Key Features

- **⚡ Ultra-Fast Processing**: 47,000+ samples per second processing speed
- **🎯 High Detection Quality**: 77.75% accuracy with 97.51% cluster quality & 79.19% F1-score
- **� Real-Time Metrics Dashboard**: Live visualization of all performance metrics
- **📈 Interactive Charts**: Performance bar chart, protocol distribution, and anomaly visualizations
- **�🔄 Optimized K-means Ensemble**: 5 different K-means models with optimized configurations (6-12 clusters)
- **✨ Cluster Quality Monitoring**: Silhouette scores displayed for model health assessment
- **🤖 Incremental Learning**: Automatically saves unique uploaded logs and retrains model after 10 uploads
- **🔍 Smart Duplicate Detection**: SHA-256 hash-based duplicate prevention (transparent to users)
- **☁️ Cloud Deployed**: Frontend on Vercel, ML API on Render for global accessibility
- **⚡ Real-time Analysis**: Instant anomaly detection results with sub-second response times
- **🎨 User-Friendly Interface**: Clean, modern web application with animated metrics cards
- **⚙️ Streamlined Preprocessing**: Optimized data pipeline for maximum performance
- **🎯 Comprehensive Scoring**: Accuracy, Precision, Recall, F1-Score, and Confidence metrics
- **📋 KDD Cup 1999 Compatible**: Industry-standard dataset support with proven results

## Performance Metrics

| Metric                | Value              | Status       |
| --------------------- | ------------------ | ------------ |
| **Processing Speed**  | 47,137 samples/sec |  Excellent   |
| **Accuracy**          | 77.75%             |  Very Good   |
| **Precision**         | 84.67%             |  Excellent   |
| **Recall**            | 74.37%             |  Good        |
| **F1-Score**          | 79.19%             |  Very Good   |
| **Cluster Quality**   | 97.51% Silhouette  |  Exceptional |

### 📊 Model Quality Metrics:

- **Individual Silhouette Scores**: 97.98%, 97.81%, 96.98%, 96.97%, 97.81%
- **Average Silhouette Score**: 97.51% (exceptional cluster quality)
- **Optimal Threshold**: 16.657554 (50th percentile - balanced detection)
- **Training Time**: ~545 seconds (9 minutes) for complete ensemble
- **Ensemble Size**: 5 optimized K-means models (6-12 clusters)

### 📊 Visualization Features:

- **Comprehensive Metrics Dashboard**: Real-time display of all performance metrics
- **Performance Charts**: Interactive bar chart showing Accuracy, Precision, Recall, and F1-Score
- **Protocol Distribution**: Visual breakdown of network protocols in anomalies
- **Anomaly Visualization**: Source bytes distribution for detected threats
- **Cluster Quality Monitoring**: Live silhouette scores for model health
- **Color-Coded Cards**: Green (≥85%), Yellow (70-85%), Red (<70%) for instant assessment

## 🛠️ Technology Stack

- **Backend API**: Python 3.12+, Flask 3.0+, Flask-CORS (deployed on Render)
- **Frontend**: Flask, HTML5, CSS3, JavaScript ES6+ (deployed on Vercel)
- **Machine Learning**: scikit-learn 1.4+, NumPy 1.26+, Pandas 2.1+
- **Visualizations**: Chart.js 4.0+ for interactive charts and graphs
- **Data Processing**: Optimized preprocessing with modern Python features
- **Model Storage**: Joblib for efficient model serialization
- **Deployment**: Vercel (Frontend) + Render (Backend API)
- **Duplicate Detection**: SHA-256 hashing for file comparison
- **UI Framework**: Bootstrap 5 Grid + Custom CSS with animations

## 🌐 Live Demo

**Production URL**: [https://anomalyze.vercel.app](https://anomalyze.vercel.app)

- Frontend hosted on Vercel (globally distributed)
- ML API hosted on Render (always-on backend)
- Upload network logs and get instant anomaly detection results

## � Quick Start

### Using the Live Application

1. **Visit the deployed application**: [https://anomalyze.vercel.app](https://anomalyze.vercel.app)
2. **Upload your network log file** (KDD Cup 1999 format)
3. **View instant analysis results** with anomaly detection and metrics
4. **Review detected anomalies** with confidence scores and severity levels

### For Developers

If you want to contribute or deploy your own instance:

- **Frontend Deployment**: Fork repo → Deploy to Vercel
- **Backend API Deployment**: Fork repo → Deploy to Render
- **Documentation**: See deployment details below

## 📋 System Requirements

### Production Environment:

- **Frontend**: Vercel (Node.js environment)
- **Backend**: Render (Python 3.12+)
- **Storage**: 2GB minimum for models and data
- **Memory**: 4GB RAM recommended for backend

### Development Environment (Optional):

- **Python 3.12 or higher** (Python 3.14 recommended)
- pip package manager
- Virtual environment support
- 4GB RAM minimum

## 🎯 How to Use

1. **Access the Application**

   - Navigate to [https://anomalyze.vercel.app](https://anomalyze.vercel.app)

2. **Prepare Your Data**

   - Format: KDD Cup 1999 network log format
   - File type: `.txt` or `.csv`
   - Sample data available in the repository

3. **Upload and Analyze**

   - Click "Choose File" and select your network log
   - Click "Analyze Network Traffic"
   - Wait for analysis (typically <1 second)

4. **Review Results**
   - View comprehensive metrics dashboard with animated cards
   - See 6 key metrics: Cluster Quality, Accuracy, Precision, Recall, F1-Score, Anomalies Found
   - Analyze interactive performance chart (bar chart)
   - Review protocol distribution (doughnut chart)
   - Examine anomaly visualization by source bytes (bar chart)
   - Check severity levels (Normal, Low, Medium, High, Critical)
   - Browse detailed anomaly table with pagination
   - Download results if needed

## 📊 Dataset

The system is designed to work with the **KDD Cup 1999** network intrusion detection dataset:

- **Training Data**: `data/KDDTrain+.txt` - Used for model training
- **Test Data**: `uploads/KDDTest.txt` - Sample test data for evaluation
- **Format**: 41 features + 1 label column representing network connection records

### Data Features Include:

- Connection duration, protocol type, network service
- Bytes transferred, connection flags
- Host-based traffic features
- Content-based features
- Time-based traffic features

## 🧠 Optimized Model Architecture

### High-Performance K-means Ensemble with Enhanced Monitoring

- **5 Optimized Models**: Diverse cluster configurations (6, 8, 10, 12 clusters) with varied random seeds
- **Majority Voting**: Simple but effective ensemble prediction for speed and reliability
- **Optimized Threshold**: Automatically tuned threshold for maximum F1-score
- **Streamlined Pipeline**: RobustScaler preprocessing for better outlier handling
- **Quality Metrics**: Silhouette scores (45-65%) for cluster quality assessment
- **Real-Time Monitoring**: Live performance metrics displayed in web dashboard

### Performance Optimizations:

1. **Enhanced Preprocessing**: RobustScaler for superior outlier detection
2. **Optimized Clustering**: 20 initializations, 500 iterations per model for convergence
3. **Two-Stage Threshold Search**: Coarse + fine-tuning for optimal precision-recall balance
4. **Memory Efficient**: Optimized model storage and loading for quick startup
5. **Vectorized Operations**: NumPy-optimized distance calculations for maximum speed
6. **Visual Analytics**: Real-time charts and metrics for instant performance assessment

## 🤖 Incremental Learning System

Anomalyze features an **automatic incremental learning system** that continuously improves the model:

### How It Works:

1. **Upload & Analysis**: User uploads network logs → system analyzes for anomalies
2. **Smart Storage**: Unique files are saved to `data/uploaded_logs/` (duplicates are detected via SHA-256 hash and skipped)
3. **Counter Tracking**: System counts unique uploads in `models/upload_counter.txt`
4. **Auto-Retraining**: After 10 unique uploads, `retrain_model.py` runs automatically in the background
5. **Model Update**: New model is trained combining original data + uploaded logs, then deployed
6. **Archiving**: Uploaded logs are moved to `archived/` folder after successful retraining

### Benefits:

- ✅ **Continuous Improvement**: Model adapts to new traffic patterns over time
- ✅ **Fully Automatic**: No manual intervention required
- ✅ **Duplicate Prevention**: SHA-256 hashing prevents storing same file multiple times
- ✅ **Transparent UX**: Users always get analysis results, storage happens in background
- ✅ **Configurable**: Adjust retraining threshold in `api_server.py` (default: 10 uploads)

### Manual Retraining:

```bash
python retrain_model.py
```

See [INCREMENTAL_LEARNING.md](INCREMENTAL_LEARNING.md) for detailed documentation.

## 📈 Performance Metrics & Benchmarks

### Real-World Performance Results:

- **Processing Speed**: 47,137 samples per second
- **Total Response Time**: <0.5 seconds for 22,544 samples
- **Memory Usage**: Efficient model loading and inference
- **Scalability**: Linear scaling with dataset size

### Accuracy Metrics:

- **Overall Accuracy**: 77.75% (very good performance)
- **Precision**: 84.67% (low false positive rate)
- **Recall**: 74.37% (catches most real anomalies)
- **F1-Score**: 79.19% (excellent precision-recall balance)
- **Cluster Quality**: 97.51% Average Silhouette (exceptional clustering)
- **Individual Silhouette Scores**: 97.98%, 97.81%, 96.98%, 96.97%, 97.81%
- **Confidence Scoring**: Distance-based confidence for each prediction
- **Real-Time Visualization**: All metrics displayed with interactive charts

## 🎯 Usage

Access the live application at [https://anomalyze.vercel.app](https://anomalyze.vercel.app):

1. **Upload File**: Click "Choose File" and select your network log (KDD Cup 1999 format)
2. **Analyze**: Click "Analyze Network Traffic" button
3. **View Results**: See real-time anomaly detection with confidence scores
4. **Review Metrics**: Check accuracy, precision, recall, and F1-score (if labels provided)
5. **Automatic Learning**: Unique files are saved for model improvement (duplicates skipped)

### API Integration

You can also integrate Anomalyze into your applications via the API:

**Endpoint**: `https://anomalyze-f7u0.onrender.com/api/predict`

```bash
curl -X POST \
  -F "file=@network_logs.txt" \
  https://anomalyze-f7u0.onrender.com/api/predict
```

Response includes:

- Detected anomalies with confidence scores
- Severity levels (Normal, Low, Medium, High, Critical)
- Comprehensive metrics: Accuracy, Precision, Recall, F1-Score (if labels provided)
- Cluster quality: Silhouette scores for model health
- Processing time and sample count
- All metrics formatted for easy visualization

## � Interactive Dashboard & Visualizations

Anomalyze features a modern, real-time dashboard with comprehensive visualizations:

### 🎯 Metrics Cards (6 Key Indicators)

1. **Cluster Quality** - Silhouette score showing model clustering health (97.51%)
2. **Accuracy** - Overall detection accuracy (77.75%)
3. **Precision** - True positive rate among predictions (84.67%)
4. **Recall** - Detection rate of actual anomalies (74.37%)
5. **F1-Score** - Harmonic mean of precision and recall (79.19%)
6. **Anomalies Found** - Total threats detected in uploaded data

**Features:**

- ✨ Animated counters (smooth count-up effect)
- 🎨 Color-coded status: Green (≥85%), Yellow (70-85%), Red (<70%)
- 💫 Pulse animation after loading
- 🎯 Hover effects for interactivity

### 📈 Interactive Charts (Chart.js)

1. **Performance Metrics Bar Chart**

   - Side-by-side comparison of all 4 key metrics
   - Color-coded bars: Cyan (Accuracy), Green (Precision), Orange (Recall), Pink (F1-Score)
   - Percentage scale (0-100%)
   - Tooltip on hover with exact values

2. **Protocol Distribution Doughnut Chart**

   - Visual breakdown of network protocols in detected anomalies
   - Multi-color palette for easy distinction
   - Interactive legend
   - Hover tooltips with counts

3. **Anomaly Visualization Bar Chart**
   - Source bytes distribution for top 25 anomalies
   - Helps identify data exfiltration patterns
   - Sorted by severity
   - Cyan gradient styling

### 🎨 UI/UX Enhancements

- **Responsive Grid Layout**: Auto-adjusts from 1-6 columns based on screen size
- **Dark Theme**: Modern purple/cyan gradient design
- **Smooth Animations**: 800ms counter animations, 500ms chart rendering
- **Lazy Loading**: Charts render progressively for faster page display
- **Pagination**: Results table with 10 rows per page
- **Details Modal**: Expandable panels for each anomaly
- **Analysis History**: Session storage of past analyses

## �📁 Project Structure

```
Anomalyze/
├── api_server.py                # Backend API server (Render deployment)
├── train_model.py               # Initial model training script
├── retrain_model.py             # Automatic retraining with uploaded data
├── optimize_threshold.py        # Threshold optimization utility
├── test_performance.py          # Performance testing and benchmarking
├── requirements.txt             # Root dependencies
├── requirements-render.txt      # Backend API dependencies
├── render.yaml                  # Render deployment config
├── vercel.json                  # Vercel deployment config
├── runtime.txt                  # Python version specification
├── README.md                    # Main documentation
├── INCREMENTAL_LEARNING.md      # Incremental learning documentation
├── api/                         # Vercel frontend
│   ├── index.py                 # Vercel entry point
│   ├── app_vercel.py            # Frontend Flask app
│   ├── requirements.txt         # Frontend dependencies
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── data/                        # Training data
│   ├── KDDTrain+.txt            # Original training dataset
│   └── uploaded_logs/           # User uploaded files
│       ├── .gitkeep
│       └── archived/            # Archived after retraining
├── models/                      # Saved models and scalers
│   ├── ensemble_models.joblib   # 5 optimized K-means models
│   ├── scaler.joblib            # StandardScaler for preprocessing
│   ├── data_columns.joblib      # Column names for consistency
│   ├── optimal_threshold.joblib # Optimized threshold
│   └── upload_counter.txt       # Tracks uploads for retraining
├── uploads/                     # Test data
│   └── KDDTest.txt
└── utils/                       # Utility modules
    └── preprocessing.py         # Optimized data preprocessing
```

## 🔄 Model Training & Optimization

### Quick Start Training:

```bash
# Train the optimized ensemble model
python train_model.py

# Optimize threshold for best accuracy
python optimize_threshold.py

# Test performance and verify metrics
python test_performance.py
```

### Advanced Training Options:

```bash
python train_model.py
```

This will:

1. Load and preprocess the training data
2. Create multiple K-means models with different configurations
3. Optimize the anomaly detection threshold
4. Save all trained components to the `models/` directory
5. Display training metrics and model quality scores

## 🚨 Anomaly Detection Process

1. **Data Ingestion**: Upload network traffic data via web interface
2. **Preprocessing**: Apply feature engineering and scaling
3. **Ensemble Prediction**: Run data through multiple K-means models
4. **Confidence Calculation**: Compute prediction confidence scores
5. **Severity Assessment**: Categorize anomalies by severity level
6. **Results Display**: Present findings with detailed metrics

## 🚀 Recent Optimizations & Improvements

### Performance Enhancements (v3.0):

- **Speed Boost**: Achieved 47,000+ samples/second processing (98x faster than typical ML inference)
- **Cluster Quality**: Achieved 97.51% average silhouette score (exceptional clustering)
- **Balanced Detection**: 77.75% accuracy, 84.67% precision, 74.37% recall, 79.19% F1-score
- **Optimized Threshold**: 16.657554 (50th percentile) for optimal precision-recall balance
- **Enhanced Preprocessing**: RobustScaler with 20 initializations, 500 iterations per model
- **Response Time**: Maintained <0.5 seconds for large datasets
- **Memory Optimization**: Streamlined model loading and inference pipeline

### Technical Improvements:

1. **Advanced Preprocessing**: RobustScaler for superior outlier handling
2. **Two-Stage Optimization**: Coarse + fine threshold search (50th percentile optimal)
3. **Diverse Ensemble**: 5 models with varied cluster counts (6, 8, 10, 12, 8)
4. **High-Quality Clustering**: Individual silhouette scores: 97.98%, 97.81%, 96.98%, 96.97%, 97.81%
5. **Enhanced Training**: 20 initializations, 500 iterations, Lloyd algorithm
6. **Optimal Threshold**: 16.657554 for balanced 84.67% precision and 74.37% recall

### Benchmark Results:

```
=== PERFORMANCE BENCHMARK ===
Processing Speed: 47,137 samples/second
Total Time: 0.478 seconds (22,544 samples)
Accuracy: 77.75%
Precision: 84.67%
Recall: 74.37%
F1-Score: 79.19%
Cluster Quality: 97.51% (Silhouette)
Status: ✓ EXCELLENT Performance
```

## 🎨 Customization

### Adding New Features

Modify `utils/preprocessing.py` to add custom network features:

```python
def create_custom_features(df):
    # Add your custom feature engineering here
    df['custom_feature'] = df['feature1'] / (df['feature2'] + 1)
    return df
```

### Adjusting Model Parameters

Edit `train_model.py` to modify K-means configurations:

```python
kmeans_configs = [
    {'n_clusters': 15, 'init': 'k-means++', 'max_iter': 1000},
    # Add more configurations
]
```

## 🐛 Troubleshooting & Performance Testing

### System Status

- **Frontend**: Check Vercel deployment status at [https://anomalyze.vercel.app](https://anomalyze.vercel.app)
- **Backend API**: Health check at [https://anomalyze-f7u0.onrender.com/health](https://anomalyze-f7u0.onrender.com/health)
- **Model Info**: API endpoint at [https://anomalyze-f7u0.onrender.com/api/model-info](https://anomalyze-f7u0.onrender.com/api/model-info)

### Common Issues

1. **Slow initial response (first upload)**

   - Render backend may be in sleep mode
   - First request can take 30-60 seconds to wake up
   - Subsequent requests are instant

2. **File format error**

   - Ensure file is in KDD Cup 1999 format
   - File should be comma-separated or tab-separated
   - Check sample data in repository for reference

3. **Upload timeout**
   - Large files (>50MB) may timeout
   - Consider splitting into smaller batches
   - Contact support for bulk processing
   - Try: Different port with `app.run(port=5001)`

### Performance Troubleshooting

| Issue    | Expected         | Actual | Solution                    |
| -------- | ---------------- | ------ | --------------------------- |
| Speed    | >30K samples/sec | <10K   | Re-run `train_model.py`     |
| Accuracy | >85%             | <80%   | Run `optimize_threshold.py` |
| F1-Score | >85%             | <70%   | Check dataset quality       |
| Memory   | <2GB             | >4GB   | Use smaller batch sizes     |

## 🚀 Deployment

Anomalyze uses a split architecture for optimal performance:

### Architecture:

- **Frontend** (Vercel): Lightweight Flask app serving UI
- **Backend API** (Render): Heavy ML processing with model inference
- **Communication**: Frontend forwards uploads to backend API via HTTP

### Deploy to Production:

#### 1. Backend API (Render)

```bash
# Push code to GitHub
git push origin main

# On Render dashboard:
1. Create New Web Service
2. Connect GitHub repository
3. Build Command: pip install -r requirements-render.txt
4. Start Command: gunicorn api_server:app
5. Set Environment: PYTHON_VERSION=3.12.0
```

#### 2. Frontend (Vercel)

```bash
# On Vercel dashboard:
1. Import GitHub repository
2. Add Environment Variable:
   ANOMALYZE_API_URL = https://your-render-url.onrender.com
3. Deploy

# Or via CLI:
vercel --prod
```

### Environment Variables:

**Vercel (Frontend)**:

- `ANOMALYZE_API_URL`: Your Render backend API URL

**Render (Backend)**:

- `PYTHON_VERSION`: 3.12.0 (or higher)

### File Structure for Deployment:

```
Root/
├── api_server.py          → Render backend
├── requirements-render.txt → Render dependencies
├── render.yaml            → Render config
├── api/                   → Vercel frontend
│   ├── index.py
│   ├── app_vercel.py
│   └── requirements.txt
├── vercel.json            → Vercel config
└── runtime.txt            → Python version
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

- KDD Cup 1999 Dataset: [http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
- scikit-learn Documentation: [https://scikit-learn.org/](https://scikit-learn.org/)
- Flask Documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)

## 👥 Authors

- **pasta-lover69** - Initial work and development

## 🙏 Acknowledgments

- KDD Cup 1999 organizers for the dataset
- scikit-learn community for the machine learning tools
- Flask community for the web framework

---

**⭐ If you find this project useful, please consider giving it a star!**
