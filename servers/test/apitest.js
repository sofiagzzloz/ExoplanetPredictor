const chai = require('chai');
const chaiHttp = require('chai-http');
const server = require('../app');  // Path to your Express app
const should = chai.should();

chai.use(chaiHttp);

describe('Articles', () => {
    // Test the PUT route
    describe('/PUT article', () => {
        it('it should UPDATE an article given the id', (done) => {
            chai.request(server)
                .put('/articles/1')
                .send({title: 'Updated Title', content: 'Updated content', author: 'Updated Author'})
                .end((err, res) => {
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('message').eql('Article updated successfully.');
                    done();
                });
        });
    });

    // Test the DELETE route
    describe('/DELETE article', () => {
        it('it should DELETE an article given the id', (done) => {
            chai.request(server)
                .delete('/articles/1')
                .end((err, res) => {
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('message').eql('Article deleted successfully.');
                    done();
                });
        });
    });
});
