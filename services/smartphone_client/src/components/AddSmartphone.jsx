import React from 'react';

const AddSmartphone = (props) => {
	return (
		<form onSubmit={ (event) => props.addSmartphone(event) }>
			<div className="field">
				<input name="name" className="input is-large" type="text" 
				placeholder="Enter a name smartphone" value={ props.name } onChange={props.handleChange} required/>
			</div>
			<div className="field">
				<input name="brand" className="input is-large" type="text" 
				placeholder="Enter an brand" value={ props.brand } onChange={props.handleChange} required/>
			</div>
			<div className="field">
				<input name="price" className="input is-large" type="number" 
				placeholder="Enter an price" value={ props.price } onChange={props.handleChange} required/>
			</div>
			<div className="field">
				<input name="color" className="input is-large" type="text" 
				placeholder="Enter an color" value={ props.color } onChange={props.handleChange} required/>
			</div>
			<div className="field">
				<input name="quantity" className="input is-large" type="number" 
				placeholder="Enter an quantity" value={ props.quantity } onChange={props.handleChange} required/>
			</div>
				<input type="submit" className="button is-primary is-large is-fullwidth"
				value="Enviar" />
		</form>
		)
};

export default AddSmartphone;