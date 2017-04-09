
import { Sharebutton } from 'react-social-sharebuttons';

class App extends React.Component {
  render() {
    let text = "LINEで送る";
    let image = "36x60";
    return (
      <Sharebutton text={text} image={image} />
    );
  }
}