import ToggleButton from "./Toggle";
const Card = (props) => {
    const { product } = props;
    return (
      <div>
        <div className="prod-card">
          <img
            src={product.product_metadata.image_url}
            alt="Product here"
          />
          <h2>{product.product_metadata.name}</h2>
          <h3>{product.product_metadata.base_color}</h3>
          <ToggleButton/>
        </div>
      </div>
    );
  };
  export default Card;