// src/components/DynamicForm.js
import React from 'react';

const DynamicForm = ({ fields, handleInputChange }) => {
    return (
        <div>
            {Object.keys(fields).map((field) => (
                <div key={field}>
                    <label htmlFor={field}>{field}</label>
                    <input
                        type="text"
                        id={field}
                        name={field}
                        onChange={handleInputChange}
                    />
                    <br />
                </div>
            ))}
        </div>
    );
};

export default DynamicForm;
