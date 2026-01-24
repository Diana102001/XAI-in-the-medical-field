// src/components/Form.js

import React from 'react';
import FormField from './FormField';

const Form = ({ formFields, handleChange, handleSubmit, errors }) => (
  <form onSubmit={handleSubmit}>
    {Object.entries(formFields).map(([name, config]) => (
      <FormField
        key={name}
        name={name}
        config={config}
        handleChange={handleChange}
        error={errors[name]}
      />
    ))}
    <button type="submit">Submit</button>
  </form>
);

export default Form;
