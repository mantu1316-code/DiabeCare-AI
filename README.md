# 🩺 Diabecare AI - Production-Ready Diabetes Predictive Engine

[![Streamlit App](https://static.streamlit.io/badge_svg.svg)](https://diabecare-ai-v7flys3yg3wa7uj9d5dd8m.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

An enterprise-grade, end-to-end Machine Learning web portal engineered to analyze clinical parameters and compute real-time diabetes risk scores. This diagnostic architecture bridges raw statistical computing with an interactive, modern micro-frontend UI layer.

🔗 **Production Live Application:** [diabecare-ai.streamlit.app](https://diabecare-ai-v7flys3yg3wa7uj9d5dd8m.streamlit.app/)

---

## 🚀 Core Architecture Features

* **Multi-Model Intelligence Layer:** Leverages production-optimized supervised learning algorithms (Logistic Regression, Support Vector Machines, and Random Forest Ensemble variants) evaluated via precise precision-recall thresholds.
* **Streamlined UI/UX Integration:** Micro-frontend interactive engine containerized via Streamlit, offering rich visual feedback matrices like real-time Gauge charts and linear feature dependency graphs.
* **Robust Constraints Processing:** Advanced input validation and validation pipelines. Key medical metrics like Glucose and BMI are strictly enforced, while missing conditional metadata vectors (Insulin, Skin Thickness) are handled cleanly to ensure system scalability without computation failures.
* **Production Deployment:** Deployed seamlessly onto Cloud-native micro-clusters with continuous integration hooked up directly to source code updates.

---

## 📊 Feature Space Matrix

The integrated diagnostic pipeline processes the following standardized clinical features:

| Parameter Specification | Classification | Analytical Scope |
| :--- | :--- | :--- |
| **Glucose Concentration** | Mandatory Baseline | Plasma glucose concentration at 2 hours in an oral glucose tolerance test. |
| **Blood Pressure** | Mandatory Baseline | Diastolic blood pressure (mm Hg). |
| **Body Mass Index (BMI)** | Critical Metric | Weight in kg/(height in m)². |
| **Age** | Demographics | Chronological profile factor for metabolic scaling. |
| **Insulin & Skin Thickness**| Conditional Vectors | Optional configuration parameters optimized for automated imputation handling. |

---

## 🛠️ Local Sandbox Execution & Setup

Follow these engineering protocols to set up and run the execution stack inside an isolated local runtime context:

### 1. Source Synchronization
Clone the active tracking branch from the remote server:
```bash
git clone [https://github.com/mantu1316-code/DiabeCare-AI.git](https://github.com/mantu1316-code/DiabeCare-AI.git)
cd DiabeCare-AI
