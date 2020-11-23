import logo from './logo.svg';
import './App.css';
import { Component } from "react"

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      logsArray: [],
    };
  }

  componentDidMount() {
    fetch('http://104.198.69.57:8080/api/logs')
      .then(response => response.json())
      .then(data => this.setState({ logsArray: data }));
  }

  render() {
    return (
      <div>
        <h1>Smart Home Door Lock Facial Authentication</h1>
        <div style={{ "display": "flex", "flexWrap": "wrap" }}>
          {this.state.logsArray.map((log, i) => (
            <div key={i}>
              <p>{log["name"]}</p>
              <img src={log["url"]} alt={"photo of " + log["name"]} style={{ "maxWidth": "300px", "maxHeight": "300px", "margin": "10px", "borderRadius": "25px" }} />
            </div>
          ))}
        </div>
      </div>
    );
  }
}

export default App;
