import * as tf from '@tensorflow/tfjs';
import * as cocoSsd from '@tensorflow-models/coco-ssd';


export default async ({ app }, inject) => {
    const loadModel = async () => {
        return await cocoSsd.load({})
    }

    inject('tf', tf)
    inject('loadModel', loadModel)
};
