const modelAlgorithms = {
    regression: [
        'LinearRegression', 'Ridge', 'Lasso', 'ElasticNet', 'DecisionTreeRegressor'
    ],
    classification: [
        'LogisticRegression', 'KNeighborsClassifier', 'SVC', 'DecisionTreeClassifier', 'RandomForestClassifier'
    ]
};

const modelParameters = {
    LinearRegression: ['fit_intercept', 'normalize'],
    Ridge: ['alpha', 'solver'],
    Lasso: ['alpha', 'max_iter'],
    ElasticNet: ['alpha', 'l1_ratio'],
    DecisionTreeRegressor: ['max_depth', 'min_samples_split'],
    LogisticRegression: ['penalty', 'C'],
    KNeighborsClassifier: ['n_neighbors', 'weights'],
    SVC: ['C', 'kernel'],
    DecisionTreeClassifier: ['max_depth', 'min_samples_split'],
    RandomForestClassifier: ['n_estimators', 'max_depth']
};

const evaluationMethods = {
    regression: ['Mean Squared Error', 'R-squared'],
    classification: ['Accuracy', 'Precision-Recall', 'ROC Curve']
};

document.addEventListener('DOMContentLoaded', function () {
    $('#feature-column-selector').select2({
        placeholder: "选择特征列",
        allowClear: true
    });
    loadDatasets();
    loadTargetColumns();
    loadFeatureColumns()
    loadModelAlgorithms();
    loadModelEvaluations();
    // 更多加载逻辑...
});

document.getElementById('task-type-selector').addEventListener('change', function () {
    // const taskType = this.value;
    loadModelAlgorithms();
    loadModelEvaluations();
});

document.addEventListener('DOMContentLoaded', function () {
    const submitBtn = document.getElementById('submit-config-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitModelConfiguration);
    }
});

// 在选择算法时调用
document.getElementById('model-algorithm-container').addEventListener('change', function (event) {
    // if (event.target.name === 'model-algorithms') {
    //     showModelParameters(event.target.value);
    // }
    if (event.target.name === 'model-algorithms') {
        const algorithm = event.target.value;
        if (event.target.checked) {
            // 显示该算法的参数
            addAlgorithmParameters(algorithm);
        } else {
            // 隐藏该算法的参数
            removeAlgorithmParameters(algorithm);
        }
    }
})



function loadDatasets() {
    // 加载数据集选项的逻辑
    // 假设数据集是静态定义的
    fetch('/api/get_databases')
        .then(response => response.json())
        .then(databases => {
            const datasetSelector = document.getElementById('dataset-selector');
            databases.forEach(dataset => {
                let option = document.createElement('option');
                option.value = dataset.id;  // 或 dataset.name，视您的需求而定
                option.textContent = dataset.name;
                option.dataset.columns = JSON.stringify(dataset.columns); // 将列信息存储在数据属性中
                datasetSelector.appendChild(option);
            });
        });
}

function loadTargetColumns() {
    // 加载目标列选项的逻辑
    // 假设目标列是静态定义的
    document.getElementById('dataset-selector').addEventListener('change', function () {
        const datasetId = this.value;
        fetch(`/api/get_dataset_columns/${datasetId}`)
            .then(response => response.json())
            .then(data => {
                const targetColumnSelector = document.getElementById('target-column-selector');
                targetColumnSelector.innerHTML = ''; // 清除现有选项
                data.columns.forEach(column => {
                    let option = document.createElement('option');
                    option.value = column;
                    option.textContent = column;
                    targetColumnSelector.appendChild(option);
                });
            })
            .catch(error => console.error('Failed to load columns:', error));
    });
}

function loadFeatureColumns() {
    document.getElementById('target-column-selector').addEventListener('change', function () {
        // 获取选中的目标列
        const selectedTargetColumn = this.value;

        // 获取数据集的所有列
        const datasetId = document.getElementById('dataset-selector').value;
        fetch(`/api/get_dataset_columns/${datasetId}`)
            .then(response => response.json())
            .then(data => {

                const featureColumnsSelector = $('#feature-column-selector');
                featureColumnsSelector.empty(); // 清空现有选项

                // 筛选出除了目标列以外的其他列
                data.columns.forEach(column => {
                    if (column !== selectedTargetColumn) {
                        if (column !== selectedTargetColumn) {
                            featureColumnsSelector.append(new Option(column, column, true, true));
                        }
                    }
                });
                featureColumnsSelector.trigger('change'); // 通知Select2更新
            })
            .catch(error => console.error('Failed to load columns:', error));
    });

}

function loadModelAlgorithms() {
    // 加载模型算法选项的逻辑
    // 根据任务类型改变模型算法选项
    const taskTypeSelector = document.getElementById('task-type-selector');
    const taskType = taskTypeSelector.value;

    const algorithms = modelAlgorithms[taskType] || [];
    const container = document.getElementById('model-algorithm-container');
    container.innerHTML = '';
    algorithms.forEach(algorithm => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'algorithm-' + algorithm;
        checkbox.name = 'model-algorithms';
        checkbox.value = algorithm;
        checkbox.className = "form-check-input";
        checkbox.style = "margin: 8px; vertical-align:middle"

        const label = document.createElement('label');
        label.htmlFor = 'algorithm-' + algorithm;
        label.textContent = algorithm;
        label.style = "margin: 8px; vertical-align:middle";

        const alg_div = document.createElement('div');

        alg_div.appendChild(checkbox)
        alg_div.appendChild(label)
        container.appendChild(alg_div)

    });

}

function loadModelEvaluations() {
    // 加载模型评估方法选项的逻辑
    // 根据任务类型改变模型评估方法选项
    const taskTypeSelector = document.getElementById('task-type-selector');
    const taskType = taskTypeSelector.value;

    const methods = evaluationMethods[taskType] || [];
    const container = document.getElementById('model-evaluation-container');
    container.innerHTML = '';
    methods.forEach(method => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'evaluation-' + method;
        checkbox.name = 'evaluation-methods';
        checkbox.value = method;
        checkbox.className = "form-check-input";
        checkbox.style = "margin: 10px; vertical-align:middle";

        const label = document.createElement('label');
        label.htmlFor = 'evaluation-' + method;
        label.textContent = method;
        label.style = "margin: 10px; vertical-align:middle";

        container.appendChild(checkbox);
        container.appendChild(label);

    });
}

function showModelParameters(algorithm) {
    const parameters = modelParameters[algorithm] || [];
    const container = document.getElementById('algorithm-parameters-container');
    container.innerHTML = '';

    parameters.forEach(param => {
        const label = document.createElement('label');
        label.textContent = algorithm + ' - ' + param;
        label.htmlFor = 'parameter-' + algorithm + '-' + param;

        const input = document.createElement('input');
        input.type = 'text';
        input.id = 'parameter-' + algorithm + '-' + param;
        input.name = 'parameters[' + algorithm + '][' + param + ']';
        input.placeholder = 'Enter ' + param;

        container.appendChild(label);
        container.appendChild(input);
    });
}

function addAlgorithmParameters(algorithm) {
    const parameters = modelParameters[algorithm] || [];
    const container = document.getElementById('algorithm-parameters-container');
    const algorithmContainer = document.createElement('div');
    algorithmContainer.id = 'parameters-for-' + algorithm;
    algorithmContainer.className = "card-body";

    const heading = document.createElement('h5');
    heading.textContent = 'Parameters for ' + algorithm;
    algorithmContainer.appendChild(heading);

    parameters.forEach(param => {
        const label = document.createElement('label');
        label.textContent = param;
        label.htmlFor = 'parameter-' + algorithm + '-' + param;

        const input = document.createElement('input');
        input.type = 'text';
        input.id = 'parameter-' + algorithm + '-' + param;
        input.name = 'parameters[' + algorithm + '][' + param + ']';
        input.placeholder = 'Enter ' + param;
        input.style = 'width:40%';
        input.className = 'form-control';

        const para_div = document.createElement('div');
        para_div.style = "margin: 10px; vertical-align:middle";

        para_div.appendChild(label);
        para_div.appendChild(input);
        algorithmContainer.appendChild(para_div);
    });

    container.appendChild(algorithmContainer);
}

function removeAlgorithmParameters(algorithm) {
    const algorithmContainer = document.getElementById('parameters-for-' + algorithm);
    if (algorithmContainer) {
        algorithmContainer.remove();
    }
}

function submitModelConfiguration() {
    // 收集和提交模型配置的逻辑
    const configuration = {
        modelName: document.getElementById('model-name').value,
        datasetId: document.getElementById('dataset-selector').value,
        // dataset_name: document.getElementById('dataset-selector').value,
        targetColumn: document.getElementById('target-column-selector').value,
        featureColumns: $('#feature-column-selector').val(),
        taskType: document.getElementById('task-type-selector').value,
        modelAlgorithms: [],
        evaluationMethods: [],
        parameters: {}
    };

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    // 收集选中的模型算法
    document.querySelectorAll('[name="model-algorithms"]:checked').forEach(checkbox => {
        configuration.modelAlgorithms.push(checkbox.value);
    });

    // 收集选中的评估方法
    document.querySelectorAll('[name="evaluation-methods"]:checked').forEach(checkbox => {
        configuration.evaluationMethods.push(checkbox.value);
    });

    // 收集算法的参数
    const algorithmContainers = document.querySelectorAll('.algorithm-parameters-container > div');
    algorithmContainers.forEach(container => {
        const algorithm = container.id.replace('parameters-for-', '');
        configuration.parameters[algorithm] = {};

        container.querySelectorAll('input').forEach(input => {
            const param = input.name.match(/\[(.*?)\]$/)[1];
            configuration.parameters[algorithm][param] = input.value;
        });
    });

    // 发送配置数据到服务器
    fetch('/api/submit_training_task', {
        method: 'POST',
        body: JSON.stringify(configuration),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/ML/training_result?task_id=' + data.task_id; // 跳转到新页面
            } else {
                alert('训练任务提交失败');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

