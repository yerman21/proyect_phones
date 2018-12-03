import React, { Component } from 'react'; // nuevo
import ReactDOM from 'react-dom';
import axios from 'axios'; // nuevo
import SmartphonesList from './components/SmartphonesList';
import AddSmartphone from './components/AddSmartphone';

// nuevo
class App extends Component {	
	constructor(){
		super();
		// nuevo
		this.state = {
			smartphones: [],
			personas: [],
			smartphone: {
				name: '',
				brand: '',
				price: '',
				color: '',
				quantity: '',
				propietario: ''
			},
			persona: {
				name: '',
				lastname: '',
				age: '',
				gender: ''				
			}
			
		};
		// limitamos el contexto de this de forma manual a travès de bind()
		this.addSmartphone = this.addSmartphone.bind(this);
		this.handleChange = this.handleChange.bind(this);
	}

	componentDidMount(){
		this.getSmartphones();
	}

	render(){
		return (
			<section className="section">
				<div className="container">
					<div className="columns is-multiline is-mobile">
						<div className="column is-half">
							
							<h1 className="title is-1">Todos los Smartphones</h1>
							
							<AddSmartphone personas={ this.state.personas } name={ this.state.smartphone.name } brand={ this.state.smartphone.brand } price={ this.state.smartphone.price } color={ this.state.smartphone.color } quantity={ this.state.smartphone.quantity } addSmartphone={ this.addSmartphone } handleChange={ this.handleChange } />
						</div>
						<div className="column is-half">
							<table className="table is-half is-hoverable is-responsive">
							<thead>
							<tr>
								<td>Smartphone</td>
								<td>Marca</td>
								<td>Precio</td>
								<td>Color</td>
								<td>Cantidad</td>
								<td>Acciones</td>
							</tr>
							</thead>							
							<tbody>
								<SmartphonesList smartphones={ this.state.smartphones } />
							</tbody>
							</table>
						</div>
					</div>
					<div className="columns is-multiline is-mobile">
						<div className="column is-half">
							<h1 className="title is-1">Todas las Personas</h1>
							<AddPersona name={ this.state.persona.name } lastname={ this.state.persona.lastname } age={ this.state.persona.age } gender={ this.state.persona.gender } addPersona={ this.addPersona } handleChange={ this.handleChange } />
						</div>
					</div>
				</div>
			</section>
			)
	}

	getSmartphones(){
		axios.get(`${process.env.REACT_APP_PHONES_SERVICE_URL}/smartphones/personas/all/telefono`)
		.then((res) => { this.setState({ smartphones: res.data.data.misCelulares }); })
		.catch((err) => { console.log(err); });
	}

	getPersonas(){
		axios.get(`${process.env.REACT_APP_PHONES_SERVICE_URL}/smartphones/personas/all`)
		.then((res) => { this.setState({ personas: res.data.data.personas }); })
		.catch((err) => { console.log(err); });
	}

	addSmartphone(event){
		event.preventDefault();

		const data = {
			name: this.state.smartphone.name,
			brand: this.state.smartphone.brand,
			price: this.state.smartphone.price,
			color: this.state.smartphone.color,
			quantity: this.state.smartphone.quantity,
			propietario: this.state.smartphone.propietario,
		};
		axios.post(`${process.env.REACT_APP_PHONES_SERVICE_URL}/smartphones`, data)
		.then( (res) => { 
			console.log(res); 
			this.getSmartphones();
			this.setState({smartphone:{ name: '', brand: '', price: '', color: '', quantity: '', propietario: ''}});
		})
		.catch( (err) => {console.log(err); });
//		console.log('Sanity check!');
		console.log(this);
	}

	handleChange(event){
		const obj = {};
		obj[event.target.name] = event.target.value;
		this.setState(obj);
	}
};

ReactDOM.render(
	<App />, 
	document.getElementById('root')
);
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA