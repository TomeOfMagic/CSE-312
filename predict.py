from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
import cv2
from detectron2.utils.visualizer import ColorMode, Visualizer


def Prediction(imgname , imgsave):

    cfg = get_cfg()

    cfg.MODEL.DEVICE = 'cpu'

    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))

    cfg.MODEL.WEIGHTS = "Model/output/model_final.pth"

    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4


    predictor = DefaultPredictor(cfg)


    classes = ['scratch', 'cloudy', 'radial', 'spot']

    
    img = cv2.imread(imgname)

    outputs = predictor(img)

    v = Visualizer(img[:, :, ::-1],
                    metadata = MetadataCatalog.get("datatest").set(thing_classes = classes),
                    scale=0.8,
                    instance_mode=ColorMode.IMAGE_BW)

    v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    cv2.imwrite(imgsave, cv2.cvtColor(v.get_image(), cv2.COLOR_BGR2RGB))
