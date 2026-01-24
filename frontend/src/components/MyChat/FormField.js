// // src/components/FormField.js

// import React from 'react';

// const FormField = ({ name, config, handleChange, error }) => {
//   const getInputType = (
//     configType) => {
//     switch (configType) {
//       case 'CharField':
//       case 'TextField':
//         return 'text';
//       case 'EmailField':
//         return 'email';
//       case 'IntegerField':
//         return 'number';
//       case 'DateField':
//         return 'date';
//       case 'file':
//         return 'file';
//       default:
//         return 'text';
//     }
//   };

//   return (
//     <div>
//       <label>{config.label}</label>
//       <input
//         type={getInputType(config.type)}
//         name={name}
//         required={config.required}
//         onChange={handleChange}
//       />
//       {error && <div className="error">{error}</div>}
//     </div>
//   );
// };

// export default FormField;

import React, { useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';

const FormField = ({ name, config, handleChange, error }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const getInputType = (configType) => {
    switch (configType) {
      case 'CharField':
      case 'TextField':
        return 'text';
      case 'EmailField':
        return 'email';
      case 'IntegerField':
        return 'number';
      case 'DateField':
        return 'date';
      default:
        return 'text';
    }
  };

  const handleDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setSelectedFile(file);
    handleChange({ target: { name, value: file, files: acceptedFiles } });

    if (file && file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
  };

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  if (config.type === 'file') {
    return (
      <div>
        <label>{config.label}</label>
        <DropzoneField onDrop={handleDrop} previewUrl={previewUrl} />
        {error && <div className="error">{error}</div>}
      </div>
    );
  }

  return (
    <div>
      <label>{config.label}</label>
      <input
        type={getInputType(config.type)}
        name={name}
        required={config.required}
        onChange={handleChange}
      />
      {error && <div className="error">{error}</div>}
    </div>
  );
};

const DropzoneField = ({ onDrop, previewUrl }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps()}
      style={{
        border: '2px dashed #ccc',
        padding: '20px',
        textAlign: 'center',
        cursor: 'pointer',
        position: 'relative',
        background: previewUrl ? `url(${previewUrl}) center/contain no-repeat` : 'none',
        minHeight: '200px',
      }}
    >
      <input {...getInputProps()} style={{ display: 'none' }} />
      {!previewUrl && (
        <p>{isDragActive ? 'Drop the file here ...' : 'Drag and drop a file here, or click to select a file'}</p>
      )}
    </div>
  );
};

export default FormField;
