import { useMemo, useState, useEffect } from "react";
import FormField from "./FormField";
import TagInput from "./TagInput";
import SignatureEditor from "./SignatureEditor";

const FIELD_TYPES = [
  { value: 'int', label: 'Integer' },
  { value: 'float', label: 'Float' },
  { value: 'long', label: 'Long' },
  { value: 'double', label: 'Double' },
  { value: 'string', label: 'String' },
  { value: 'boolean', label: 'Boolean' },
  { value: 'datetime', label: 'Datetime' },
  { value: 'image', label: 'Image' },
  { value: 'video', label: 'Video' },
];

const initialInputSignature = "[]";
const initialOutputSignature = "[]";

export default function AIModelForm() {
  const [name, setName] = useState("");
  const [modelURI, setModelURI] = useState("");
  const [flavor, setFlavor] = useState("keras");
  const [classificationType, setClassificationType] = useState("binary");
  const [datasetPath, setDatasetPath] = useState("");
  const [numLabels, setNumLabels] = useState(2);
  const [minLabels, setMinLabels] = useState(1);
  const [maxLabels, setMaxLabels] = useState(1);
  const [labels, setLabels] = useState(["yes", "no"]);
  const [sourceType, setSourceType] = useState("code");
  const [codeSnippet, setCodeSnippet] = useState("");
  const [modelFile, setModelFile] = useState(null);
  const [inputFields, setInputFields] = useState([]);
  const [outputFields, setOutputFields] = useState([]);
  const [inputSignature, setInputSignature] = useState(initialInputSignature);
  const [outputSignature, setOutputSignature] = useState(initialOutputSignature);
  const [lastPayload, setLastPayload] = useState(null);
  const [formError, setFormError] = useState(null);

  const addInputField = () => {
    setInputFields([...inputFields, {
      name: '',
      type: 'string',
      required: false,
      min_value: '',
      max_value: '',
      data_type: '',
      batch_size: '',
      rgb: false,
      width: '',
      height: '',
      num_channels: '',
      num_frames: '',
    }]);
  };

  const removeInputField = (index) => {
    setInputFields(inputFields.filter((_, i) => i !== index));
  };

  const updateInputField = (index, key, value) => {
    const newFields = [...inputFields];
    newFields[index][key] = value;
    setInputFields(newFields);
  };

  const addOutputField = () => {
    setOutputFields([...outputFields, {
      name: '',
      type: 'string',
      required: false,
      min_value: '',
      max_value: '',
      data_type: '',
      batch_size: '',
      rgb: false,
      width: '',
      height: '',
      num_channels: '',
      num_frames: '',
    }]);
  };

  const removeOutputField = (index) => {
    setOutputFields(outputFields.filter((_, i) => i !== index));
  };

  const updateOutputField = (index, key, value) => {
    const newFields = [...outputFields];
    newFields[index][key] = value;
    setOutputFields(newFields);
  };

  const isNumericType = (type) => ["int", "long", "float", "double"].includes(type);
  const isImageType = (type) => type === "image";
  const isVideoType = (type) => type === "video";

  useEffect(() => {
    setNumLabels(labels.length);
  }, [labels]);

  useEffect(() => {
    try {
      const parsed = JSON.stringify(inputFields, null, 2);
      setInputSignature(parsed);
    } catch (error) {
      // ignore
    }
  }, [inputFields]);

  useEffect(() => {
    try {
      const parsed = JSON.stringify(outputFields, null, 2);
      setOutputSignature(parsed);
    } catch (error) {
      // ignore
    }
  }, [outputFields]);

  useEffect(() => {
    if (classificationType === "binary") {
      setNumLabels(2);
      setMinLabels(1);
      setMaxLabels(1);
      setLabels(labels.length === 2 ? labels : ["yes", "no"]);
    } else if (classificationType === "multi_classes") {
      setMinLabels(1);
      setMaxLabels(Math.max(2, numLabels));
      if (labels.length < 2) {
        setLabels(["class1", "class2"]);
        setNumLabels(2);
      }
    } else if (classificationType === "multi_labels") {
      setMinLabels(1);
      setMaxLabels(Math.max(1, numLabels));
      if (labels.length < 1) {
        setLabels(["label1"]);
        setNumLabels(1);
      }
    }
  }, [classificationType]);

  const parseSignature = (signatureString, fallback) => {
    if (!signatureString || signatureString.trim() === "") {
      return fallback;
    }

    try {
      const parsed = JSON.parse(signatureString);
      if (Array.isArray(parsed)) {
        return parsed;
      }
      if (parsed && typeof parsed === "object" && Object.keys(parsed).length > 0) {
        return parsed;
      }
      // empty object/array should fallback to explicit fields if provided
      return fallback;
    } catch (_error) {
      return fallback;
    }
  };

  const payloadPreview = useMemo(
    () => ({
      modelURI: modelURI || "local://model-1",
      name: name || "Untitled model",
      flavor,
      classification_type: classificationType,
      dataset_path: datasetPath || null,
      labels: {
        num_labels: numLabels,
        label_names: labels,
        min_labels: minLabels,
        max_labels: maxLabels,
      },
      input_signature: parseSignature(inputSignature, inputFields),
      output_signature: parseSignature(outputSignature, outputFields),
    }),
    [
      modelURI,
      name,
      flavor,
      classificationType,
      datasetPath,
      numLabels,
      minLabels,
      maxLabels,
      labels,
      inputFields,
      outputFields,
    ]
  );

  const handleSubmit = async (event) => {
    event.preventDefault();

    setFormError(null);

    let inputSignatureValue = parseSignature(inputSignature, inputFields);
    let outputSignatureValue = parseSignature(outputSignature, outputFields);

    if (inputSignature.trim() !== "" && inputSignatureValue === inputFields && inputSignature !== JSON.stringify(inputFields, null, 2)) {
      setFormError("Input signature contains invalid JSON. Please fix it before submitting.");
      return;
    }

    if (outputSignature.trim() !== "" && outputSignatureValue === outputFields && outputSignature !== JSON.stringify(outputFields, null, 2)) {
      setFormError("Output signature contains invalid JSON. Please fix it before submitting.");
      return;
    }

    const effectiveModelURI = modelURI?.trim() || `local://model-${Date.now()}`;

    const payload = {
      modelURI: effectiveModelURI,
      name: name || "Untitled model",
      flavor,
      classification_type: classificationType,
      dataset_path: datasetPath || null,
      labels: {
        num_labels: numLabels,
        label_names: labels,
        min_labels: minLabels,
        max_labels: maxLabels,
      },
      input_signature: inputSignatureValue,
      output_signature: outputSignatureValue,
      source_type: sourceType,
      code_snippet: sourceType === "code" ? codeSnippet : "",
    };

    setLastPayload(payload);

    const formData = new FormData();
    formData.append("data", JSON.stringify(payload));
    if (modelFile) {
      formData.append("file", modelFile);
    }

    try {
      const response = await fetch("/api/ai/models/", {
        method: "POST",
        body: formData,
      });

      const responseText = await response.text();
      let responseJson = null;
      try {
        responseJson = JSON.parse(responseText);
      } catch {
        responseJson = responseText;
      }

      if (!response.ok) {
        const errorMessage = responseJson?.error || responseJson?.detail || responseText || "Unknown error";
        setFormError(`Model save failed: ${errorMessage}`);
        console.error("Failed to create model", responseJson);
        return;
      }

      setFormError(null);
      console.log("Model created successfully", responseJson);
      setLastPayload(responseJson);
      setModelURI(effectiveModelURI);

    } catch (error) {
      console.error("Model creation error", error);
    }
  };

  return (
    <div className="grid">
      <section className="card">
        <div className="card-head">
          <div>
            <h2>Create an AI Model</h2>
            <p>Register a model, define its schema, and keep everything traceable.</p>
          </div>
          <span className="pill">Step 1 of 1</span>
        </div>

        {formError && (
          <div className="error" style={{ color: "#b00020", marginBottom: "10px", fontWeight: "600" }}>
            {formError}
          </div>
        )}

        <form className="form" onSubmit={handleSubmit}>
          <div className="two-col">
            <FormField label="Model name" hint="A friendly identifier for your team.">
              <input
                className="input"
                placeholder="Cardio Risk v3"
                value={name}
                onChange={(event) => setName(event.target.value)}
              />
            </FormField>

            <FormField label="Model URI" hint="Storage pointer or registry reference.">
              <input
                className="input"
                placeholder="s3://models/cardio-risk-v3"
                value={modelURI}
                onChange={(event) => setModelURI(event.target.value)}
              />
            </FormField>
          </div>

          <div className="two-col">
            <FormField label="Framework flavor" hint="Which runtime should load it?">
              <select
                className="input"
                value={flavor}
                onChange={(event) => setFlavor(event.target.value)}
              >
                <option value="keras">Keras</option>
                <option value="pytorch">PyTorch</option>
              </select>
            </FormField>

            <FormField label="Classification type" hint="Binary, multi-class, or multi-label.">
              <select
                className="input"
                value={classificationType}
                onChange={(event) => setClassificationType(event.target.value)}
              >
                <option value="binary">Binary</option>
                <option value="multi_classes">Multi Classes</option>
                <option value="multi_labels">Multi Labels</option>
              </select>
            </FormField>
          </div>

          <div className="two-col">
            <FormField label="Number of Labels" hint="Total labels for the model.">
              <input
                className="input"
                type="number"
                min="0"
                value={numLabels}
                onChange={(event) => setNumLabels(parseInt(event.target.value, 10) || 0)}
              />
            </FormField>

            <FormField label="Minimum Labels" hint="Min labels per prediction.">
              <input
                className="input"
                type="number"
                min="0"
                value={minLabels}
                onChange={(event) => setMinLabels(parseInt(event.target.value, 10) || 0)}
              />
            </FormField>
          </div>

          <FormField label="Maximum Labels" hint="Max labels per prediction.">
            <input
              className="input"
              type="number"
              min="0"
              value={maxLabels}
              onChange={(event) => setMaxLabels(parseInt(event.target.value, 10) || 0)}
            />
          </FormField>

          <FormField label="Source Type" hint="How to provide the model.">
            <select
              className="input"
              value={sourceType}
              onChange={(event) => setSourceType(event.target.value)}
            >
              <option value="code">Code Snippet</option>
              <option value="file">File Upload</option>
            </select>
          </FormField>

          {sourceType === "code" && (
            <FormField label="Code Snippet" hint="Model loading code.">
              <textarea
                className="input"
                rows="5"
                value={codeSnippet}
                onChange={(event) => setCodeSnippet(event.target.value)}
                placeholder="model = load_model('path/to/model')"
              />
            </FormField>
          )}

          {sourceType === "file" && (
            <FormField label="Model File" hint="Upload the model file.">
              <input
                className="input"
                type="file"
                onChange={(event) => setModelFile(event.target.files[0])}
              />
            </FormField>
          )}

          <FormField label="Dataset path" hint="Optional path for reproducibility.">
            <input
              className="input"
              placeholder="data/clean/clinical.csv"
              value={datasetPath}
              onChange={(event) => setDatasetPath(event.target.value)}
            />
          </FormField>

          <TagInput
            label="Labels"
            placeholder="Add label"
            value={labels}
            onChange={setLabels}
            maxTags={classificationType === "binary" ? 2 : undefined}
          />

          <div className="form-group">
            <h3>Input Fields</h3>
            {inputFields.map((field, index) => (
              <div key={index} className="field-row" style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
                <FormField label="Name">
                  <input
                    className="input"
                    value={field.name}
                    onChange={(e) => updateInputField(index, 'name', e.target.value)}
                  />
                </FormField>
                <FormField label="Type">
                  <select
                    className="input"
                    value={field.type}
                    onChange={(e) => updateInputField(index, 'type', e.target.value)}
                  >
                    {FIELD_TYPES.map((type) => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </select>
                </FormField>
                <FormField label="Required">
                  <input
                    type="checkbox"
                    checked={field.required}
                    onChange={(e) => updateInputField(index, 'required', e.target.checked)}
                  />
                </FormField>

                {isNumericType(field.type) && (
                  <>
                    <FormField label="Min Value">
                      <input
                        className="input"
                        type="number"
                        value={field.min_value}
                        onChange={(e) => updateInputField(index, 'min_value', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Max Value">
                      <input
                        className="input"
                        type="number"
                        value={field.max_value}
                        onChange={(e) => updateInputField(index, 'max_value', e.target.value)}
                      />
                    </FormField>
                  </>
                )}

                {isImageType(field.type) && (
                  <>
                    <FormField label="Data Type">
                      <input
                        className="input"
                        value={field.data_type}
                        onChange={(e) => updateInputField(index, 'data_type', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Batch Size">
                      <input
                        className="input"
                        type="number"
                        value={field.batch_size}
                        onChange={(e) => updateInputField(index, 'batch_size', e.target.value)}
                      />
                    </FormField>
                    <FormField label="RGB">
                      <input
                        type="checkbox"
                        checked={field.rgb}
                        onChange={(e) => updateInputField(index, 'rgb', e.target.checked)}
                      />
                    </FormField>
                    <FormField label="Width">
                      <input
                        className="input"
                        type="number"
                        value={field.width}
                        onChange={(e) => updateInputField(index, 'width', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Height">
                      <input
                        className="input"
                        type="number"
                        value={field.height}
                        onChange={(e) => updateInputField(index, 'height', e.target.value)}
                      />
                    </FormField>
                  </>
                )}

                {isVideoType(field.type) && (
                  <>
                    <FormField label="Data Type">
                      <input
                        className="input"
                        value={field.data_type}
                        onChange={(e) => updateInputField(index, 'data_type', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Batch Size">
                      <input
                        className="input"
                        type="number"
                        value={field.batch_size}
                        onChange={(e) => updateInputField(index, 'batch_size', e.target.value)}
                      />
                    </FormField>
                    <FormField label="RGB">
                      <input
                        type="checkbox"
                        checked={field.rgb}
                        onChange={(e) => updateInputField(index, 'rgb', e.target.checked)}
                      />
                    </FormField>
                    <FormField label="Width">
                      <input
                        className="input"
                        type="number"
                        value={field.width}
                        onChange={(e) => updateInputField(index, 'width', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Height">
                      <input
                        className="input"
                        type="number"
                        value={field.height}
                        onChange={(e) => updateInputField(index, 'height', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Num Channels">
                      <input
                        className="input"
                        type="number"
                        value={field.num_channels}
                        onChange={(e) => updateInputField(index, 'num_channels', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Num Frames">
                      <input
                        className="input"
                        type="number"
                        value={field.num_frames}
                        onChange={(e) => updateInputField(index, 'num_frames', e.target.value)}
                      />
                    </FormField>
                  </>
                )}

                <button type="button" onClick={() => removeInputField(index)}>Remove</button>
              </div>
            ))}
            <button type="button" onClick={addInputField}>Add Input Field</button>
          </div>

          <div className="form-group">
            <h3>Output Fields</h3>
            {outputFields.map((field, index) => (
              <div key={index} className="field-row" style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
                <FormField label="Name">
                  <input
                    className="input"
                    value={field.name}
                    onChange={(e) => updateOutputField(index, 'name', e.target.value)}
                  />
                </FormField>
                <FormField label="Type">
                  <select
                    className="input"
                    value={field.type}
                    onChange={(e) => updateOutputField(index, 'type', e.target.value)}
                  >
                    {FIELD_TYPES.map((type) => (
                      <option key={type.value} value={type.value}>{type.label}</option>
                    ))}
                  </select>
                </FormField>
                <FormField label="Required">
                  <input
                    type="checkbox"
                    checked={field.required}
                    onChange={(e) => updateOutputField(index, 'required', e.target.checked)}
                  />
                </FormField>

                {isNumericType(field.type) && (
                  <>
                    <FormField label="Min Value">
                      <input
                        className="input"
                        type="number"
                        value={field.min_value}
                        onChange={(e) => updateOutputField(index, 'min_value', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Max Value">
                      <input
                        className="input"
                        type="number"
                        value={field.max_value}
                        onChange={(e) => updateOutputField(index, 'max_value', e.target.value)}
                      />
                    </FormField>
                  </>
                )}

                {isImageType(field.type) && (
                  <>
                    <FormField label="Data Type">
                      <input
                        className="input"
                        value={field.data_type}
                        onChange={(e) => updateOutputField(index, 'data_type', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Batch Size">
                      <input
                        className="input"
                        type="number"
                        value={field.batch_size}
                        onChange={(e) => updateOutputField(index, 'batch_size', e.target.value)}
                      />
                    </FormField>
                    <FormField label="RGB">
                      <input
                        type="checkbox"
                        checked={field.rgb}
                        onChange={(e) => updateOutputField(index, 'rgb', e.target.checked)}
                      />
                    </FormField>
                    <FormField label="Width">
                      <input
                        className="input"
                        type="number"
                        value={field.width}
                        onChange={(e) => updateOutputField(index, 'width', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Height">
                      <input
                        className="input"
                        type="number"
                        value={field.height}
                        onChange={(e) => updateOutputField(index, 'height', e.target.value)}
                      />
                    </FormField>
                  </>
                )}

                {isVideoType(field.type) && (
                  <>
                    <FormField label="Data Type">
                      <input
                        className="input"
                        value={field.data_type}
                        onChange={(e) => updateOutputField(index, 'data_type', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Batch Size">
                      <input
                        className="input"
                        type="number"
                        value={field.batch_size}
                        onChange={(e) => updateOutputField(index, 'batch_size', e.target.value)}
                      />
                    </FormField>
                    <FormField label="RGB">
                      <input
                        type="checkbox"
                        checked={field.rgb}
                        onChange={(e) => updateOutputField(index, 'rgb', e.target.checked)}
                      />
                    </FormField>
                    <FormField label="Width">
                      <input
                        className="input"
                        type="number"
                        value={field.width}
                        onChange={(e) => updateOutputField(index, 'width', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Height">
                      <input
                        className="input"
                        type="number"
                        value={field.height}
                        onChange={(e) => updateOutputField(index, 'height', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Num Channels">
                      <input
                        className="input"
                        type="number"
                        value={field.num_channels}
                        onChange={(e) => updateOutputField(index, 'num_channels', e.target.value)}
                      />
                    </FormField>
                    <FormField label="Num Frames">
                      <input
                        className="input"
                        type="number"
                        value={field.num_frames}
                        onChange={(e) => updateOutputField(index, 'num_frames', e.target.value)}
                      />
                    </FormField>
                  </>
                )}

                <button type="button" onClick={() => removeOutputField(index)}>Remove</button>
              </div>
            ))}
            <button type="button" onClick={addOutputField}>Add Output Field</button>
          </div>

          <div className="two-col">
            <SignatureEditor
              label="Input signature"
              value={inputSignature}
              onChange={setInputSignature}
              hint="JSON describing the expected input shape."
            />
            <SignatureEditor
              label="Output signature"
              value={outputSignature}
              onChange={setOutputSignature}
              hint="JSON describing the model outputs."
            />
          </div>

          <div className="actions">
            <button className="btn" type="submit">
              Create model payload
            </button>
            <button
              className="btn ghost"
              type="button"
              onClick={() => setLastPayload(null)}
            >
              Reset preview
            </button>
          </div>
        </form>
      </section>

      <section className="card muted">
        <h3>Payload preview</h3>
        <p>
          This is the body you can send to your `POST /api/ai/models/` endpoint.
        </p>
        <pre className="code">
          {JSON.stringify(lastPayload ?? payloadPreview, null, 2)}
        </pre>
      </section>
    </div>
  );
}

function safeParse(value) {
  try {
    return JSON.parse(value);
  } catch (error) {
    return value;
  }
}
