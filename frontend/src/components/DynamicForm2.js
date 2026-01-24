// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import { useParams } from 'react-router-dom';
// const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

// const DynamicForm = () => {
//   const { modelid } = useParams();
//   const [formFields, setFormFields] = useState({});
//   const [formData, setFormData] = useState({});
//   const [result, setResult] = useState(null);
//   const [errors, setErrors] = useState({});

//   useEffect(() => {
//     axios.get(`${API_BASE_URL}/dynamic-form/${modelid}/`)
//       .then(response => {
//         setFormFields(response.data.form);
//       })
//       .catch(error => {
//         console.error('There was an error fetching the form schema!', error);
//       });
//   }, [modelid]);

//   const handleChange = (e) => {
//     const { name, value, files } = e.target;
//     if (files) {
//       setFormData({
//         ...formData,
//         [name]: files[0]
//       });
//     } else {
//       setFormData({
//         ...formData,
//         [name]: value
//       });
//     }
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     const formDataToSend = new FormData();
//     for (const key in formData) {
//       formDataToSend.append(key, formData[key]);
//     }

//     axios.post(`${API_BASE_URL}/dynamic-form/${modelid}/`, formDataToSend)
//       .then(response => {
//         setResult(response.data.result);
//         setErrors({});
//       })
//       .catch(error => {
//         if (error.response && error.response.data) {
//           setErrors(error.response.data.errors);
//         } else {
//           console.error('There was an error submitting the form!', error);
//         }
//       });
//   };

//   return (
//     <div>
//       <h1>Dynamic Form</h1>
//       <form onSubmit={handleSubmit}>
//         {Object.entries(formFields).map(([name, config]) => (
//           <div key={name}>
//             <label>{config.label}</label>
//             <input
//               type={config.type === 'ImageField' ? 'file' : 'text'}
//               name={name}
//               required={config.required}
//               onChange={handleChange}
//             />
//             {errors[name] && <div className="error">{errors[name]}</div>}
//           </div>
//         ))}
//         <button type="submit">Submit</button>
//       </form>
//       {result && (
//         <div>
//           <h2>Result</h2>
//           <pre>{JSON.stringify(result, null, 2)}</pre>
//         </div>
//       )}
//     </div>
//   );
// };

// export default DynamicForm;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:8000'; // Adjust the base URL as needed

const DynamicForm = () => {
  const { modelid } = useParams();
  const [formFields, setFormFields] = useState({});
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [errors, setErrors] = useState({});
  const [explanation, setExplanation] = useState(null);
  const [queryId, setQueryId] = useState(null);


  useEffect(() => {
    axios.get(`${API_BASE_URL}/dynamic-form/${modelid}/`)
      .then(response => {
        setFormFields(response.data.form);
      })
      .catch(error => {
        console.error('There was an error fetching the form schema!', error);
      });
  }, [modelid]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (files) {
      setFormData({
        ...formData,
        [name]: files[0]
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formDataToSend = new FormData();
    for (const key in formData) {
      formDataToSend.append(key, formData[key]);
    }

    axios.post(`${API_BASE_URL}/dynamic-form/${modelid}/`, formDataToSend)
      .then(response => {
        setResult(response.data.result);
        setErrors({});
        setExplanation(null);  // Reset explanation when a new result is fetched
        setQueryId(response.data.query_id);  // Store the query_id

      })
      .catch(error => {
        if (error.response && error.response.data) {
          setErrors(error.response.data.errors);
        } else {
          console.error('There was an error submitting the form!', error);
        }
      });
  };

  const getInputType = (configType) => {
    switch(configType) {
      case 'CharField':
      case 'TextField':
        return 'text';
      case 'EmailField':
        return 'email';
      case 'IntegerField':
        return 'number';
      case 'DateField':
        return 'date';
      case 'file':
        return 'file';
      default:
        return 'text';
    }
  };
  const getExplanation = () => {
    if (!queryId) {
      console.error('Query ID is not available.');
      return;
    }

    axios.get(`${API_BASE_URL}/dynamic-form/${modelid}/${queryId}/`)
      .then(response => {
        setExplanation(response.data.explanation);
      })
      .catch(error => {
        console.error('There was an error fetching the explanation!', error);
      });
  };

  return (
    <div>
      <h1>Dynamic Form</h1>
      <form onSubmit={handleSubmit}>
        {Object.entries(formFields).map(([name, config]) => (
          <div key={name}>
            <label>{config.label}</label>
            <input
              type={getInputType(config.type)}
              name={name}
              required={config.required}
              onChange={handleChange}
            />
            {errors[name] && <div className="error">{errors[name]}</div>}
          </div>
        ))}
        <button type="submit">Submit</button>
      </form>
      {result && (
        <div>
          <h2>Result</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
          <button type="button" onClick={getExplanation}>Explain</button>
        </div>
      )}
       {explanation && (
      <div>
        <h2>Explanation</h2>
        <pre>{JSON.stringify(explanation, null, 2)}</pre>
      </div>
    )}
    </div>
  );
};

export default DynamicForm;
