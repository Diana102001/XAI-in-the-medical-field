// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// // Base URL for the API
// const API_BASE_URL = 'http://localhost:8000';

// const Explanation = ({ modelid, queryId }) => {
//   // State to hold the explanation data and loading/error states
//   const [explanation, setExplanation] = useState('');
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     // Function to fetch explanation from the API
//     const fetchExplanation = async () => {
//       try {
//         // Construct the API URL
//         const url = `${API_BASE_URL}/dynamic-form/${modelid}/${queryId}/`;
        
//         // Fetch data from the API
//         const response = await axios.get(url);

//         // Update state with the fetched explanation
//         setExplanation(response.data.explanation);
//       } catch (error) {
//         // Handle errors
//         console.error('There was an error fetching the Explanation', error);
//         setError('There was an error fetching the explanation.');
//       } finally {
//         // Set loading to false when done
//         setLoading(false);
//       }
//     };

//     // Fetch the explanation when modelid or queryId changes
//     fetchExplanation();
//   }, [modelid, queryId]);

//   // Render loading, error, or explanation based on the state
//   if (loading) {
//     return <p>Loading...</p>;
//   }

//   if (error) {
//     return <p>{error}</p>;
//   }

//   return (
//     <div>
//       <h3>Explanation for Model {modelid}</h3>
//       <p>Based on Query ID: {queryId}</p>
//       <pre>{JSON.stringify(explanation, null, 2)}</pre>
//       {/* Add logic to display the explanation based on modelid and queryId */}
//     </div>
//   );
// };

// export default Explanation;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ExplanationItem from './ExplanationItem';
import './Explanation.css';

const API_BASE_URL = 'http://localhost:8000';

const Explanation = ({ modelid, queryId }) => {
  const [explanation, setExplanation] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [explanation_ids,setExplanationIds]=useState({})

  useEffect(() => {
    const fetchExplanation = async () => {
      try {
        const url = `${API_BASE_URL}/dynamic-form/${modelid}/${queryId}/`;
        const response = await axios.get(url);
        setExplanation(response.data.explanation);
        setExplanationIds(response.data.explanation_ids)
      } catch (error) {
        console.error('There was an error fetching the explanation', error);
        setError('There was an error fetching the explanation.');
      } finally {
        setLoading(false);
      }
    };

    fetchExplanation();
  }, [modelid, queryId]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      
      <div className="explanation-container">
        {Object.entries(explanation).map(([key, value],index) => (
          <ExplanationItem
            explanationId={explanation_ids[index]}
            explanationKey={key}
            explanationValue={value}
          />
        ))}
      </div>
    </div>
  );
};

export default Explanation;
