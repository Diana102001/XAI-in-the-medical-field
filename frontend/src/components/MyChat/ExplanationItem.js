import React from 'react';
import StarRating from './StarRating';

const ExplanationItem = ({ explanationId, explanationKey, explanationValue }) => {
  return (
    <div className="explanation-item">
      <h4>{explanationKey}</h4>
      <p>{explanationValue}</p>
      <StarRating explanationId={explanationId} />
    </div>
  );
};

export default ExplanationItem;
