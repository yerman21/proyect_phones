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
			name: '',
			brand: '',
			price: '',
			color: '',
			quantity: ''
		};
		// limitamos el contexto de this de forma manual a travès de bind()
		this.addSmartphone = this.addSmartphone.bind(this); //new
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
							
							<AddSmartphone name={ this.state.name } brand={ this.state.brand } price={ this.state.price } color={ this.state.color } quantity={ this.state.quantity } addSmartphone={ this.addSmartphone } handleChange={ this.handleChange } />
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
				</div>
			</section>
			)
	}

	getSmartphones(){
		axios.get(`${process.env.REACT_APP_PHONES_SERVICE_URL}/smartphones`)
		.then((res) => { this.setState({ smartphones: res.data.data.smartphones }); })
		.catch((err) => { console.log(err); });
	}

	addSmartphone(event){
		event.preventDefault();

		const data = {
			name: this.state.name,
			brand: this.state.brand,
			price: this.state.price,
			color: this.state.color,
			quantity: this.state.quantity,
		};
		axios.post(`${process.env.REACT_APP_PHONES_SERVICE_URL}/smartphones`, data)
		.then( (res) => { 
			console.log(res); 
			this.getSmartphones();
			this.setState({ name: '', brand: '', price: '', color: '', quantity: '' });
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