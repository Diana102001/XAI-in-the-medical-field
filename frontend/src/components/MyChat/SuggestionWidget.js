import React from 'react';

const SuggestionWidget = ({ suggestion, onClick }) => {
  return (
    <div className="suggestion-widget">
      <button onClick={() => onClick(suggestion)}>
        {suggestion}
      </button>
    </div>
  );
};

export default SuggestionWidget;
